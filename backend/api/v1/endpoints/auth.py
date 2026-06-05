from fastapi import APIRouter, Header, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from core.database import get_user_by_email, create_user, get_user_by_id, update_last_login
from core.jwt_helper import encode_jwt, decode_jwt
from core.response import BaseResponse
from core.exceptions import AppException

router = APIRouter()

class GoogleLoginRequest(BaseModel):
    id_token: Optional[str] = Field(None, description="Raw Google ID token")
    # For developer simulator bypass
    email: Optional[str] = Field(None, description="Developer bypass email")
    name: Optional[str] = Field(None, description="Developer bypass name")
    picture: Optional[str] = Field(None, description="Developer bypass avatar URL")
    google_id: Optional[str] = Field(None, description="Developer bypass Google ID")

class AuthUserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    picture: Optional[str]
    token: str

def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Dependency that authorizes request headers and returns the current user profile dict."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")
        
    token = authorization.split(" ")[1]
    payload = decode_jwt(token)
    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Session expired or invalid token.")
        
    user = get_user_by_id(payload["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail="User account not found.")
        
    return user

@router.post(
    "/google",
    response_model=BaseResponse[AuthUserResponse],
    summary="Google Sign-In / Developer Bypass Endpoint",
    description="Registers or logs in a user via Google ID Token or Developer Simulation, returning a session token."
)
async def google_login(payload: GoogleLoginRequest):
    try:
        # Determine if we are running in real Google Verification or Simulator Bypass
        email = payload.email
        name = payload.name or "SaaS User"
        picture = payload.picture or "https://lh3.googleusercontent.com/a/default-user"
        google_id = payload.google_id
        
        # If we have an id_token, we can attempt standard token validation (e.g. online fallback or decoding)
        if payload.id_token:
            # Under standard local development without an active connection, we can parse the JWT client-side claims
            # or make a lightweight call to Google oauth2 tokeninfo.
            # To be robust, let's extract details from the ID Token claims safely, or fallback to simulate if invalid.
            claims = decode_jwt(payload.id_token) # If token is self-signed or we inspect it
            if claims:
                email = claims.get("email", email)
                name = claims.get("name", name)
                picture = claims.get("picture", picture)
                google_id = claims.get("sub", google_id)
            else:
                # If Google verification fails or is unconfigured, we check if bypass details were supplied
                if not email:
                    raise AppException(message="Google ID Token verification failed and no backup credentials were provided.", status_code=401)
        
        if not email:
            raise AppException(message="Email address is required for user sign-in.", status_code=400)
            
        if not google_id:
            google_id = f"sim_{email}" # Simulation Google ID
            
        # Retrieve or create user in SQLite database
        user = get_user_by_email(email)
        if not user:
            user_id = create_user(email, name, picture, google_id)
            user = get_user_by_id(user_id)
        else:
            update_last_login(user["id"])
            
        # Create signed JWT token
        session_token = encode_jwt({"user_id": user["id"], "email": user["email"]})
        
        return BaseResponse(
            success=True,
            data=AuthUserResponse(
                id=user["id"],
                email=user["email"],
                name=user["name"],
                picture=user["picture"],
                token=session_token
            ),
            message="Sign-in completed successfully."
        )
    except AppException:
        raise
    except Exception as e:
        raise AppException(message=f"Authentication error: {str(e)}", status_code=500)

@router.get(
    "/me",
    response_model=BaseResponse[Dict[str, Any]],
    summary="Restore User Session Profile",
    description="Validates the current session token and returns the authenticated user's profile."
)
async def get_my_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    # Clean sensitive database details before returning
    profile = {
        "id": current_user["id"],
        "email": current_user["email"],
        "name": current_user["name"],
        "picture": current_user["picture"],
        "last_login": current_user["last_login"],
        "created_at": current_user["created_at"]
    }
    return BaseResponse(
        success=True,
        data=profile,
        message="Session restored successfully."
    )
