import jwt
from typing import Dict, Any, Optional
from core.config import settings
from supabase import create_client, Client

# Initialize the Supabase client
# Wrap in try/except so it doesn't crash on startup if URL/key is unconfigured
try:
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
except Exception as e:
    print(f"WARNING: Supabase client initialization failed: {str(e)}")
    supabase = None

def verify_supabase_jwt(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes and validates a Supabase JWT token signature and expiry.
    Returns payload dict if valid, or None if invalid.
    Includes a developer simulation bypass for offline development.
    """
    # 1. Developer simulation bypass
    if token.startswith("sim_token_"):
        email = token.replace("sim_token_", "")
        # Create a deterministic UUID based on email hash
        import hashlib
        email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
        sim_uuid = f"00000000-0000-0000-0000-{email_hash[:12]}"
        return {
            "sub": sim_uuid,
            "email": email,
            "role": "authenticated",
            "user_metadata": {
                "full_name": email.split("@")[0].capitalize(),
                "avatar_url": "https://lh3.googleusercontent.com/a/default-user"
            }
        }

    # 2. Real JWT Decode & Verify
    try:
        unverified_header = jwt.get_unverified_header(token)
        alg = unverified_header.get("alg", "HS256")
        
        if alg == "HS256":
            # Supabase HS256 secrets are base64-encoded. We attempt decoding it,
            # but keep the raw string as a fallback.
            secrets_to_try = [settings.SUPABASE_JWT_SECRET]
            try:
                import base64
                cleaned_secret = settings.SUPABASE_JWT_SECRET.strip()
                # Pad base64 if needed
                padded_secret = cleaned_secret + "=" * ((4 - len(cleaned_secret) % 4) % 4)
                decoded_bytes = base64.b64decode(padded_secret)
                if decoded_bytes:
                    secrets_to_try.append(decoded_bytes)
            except Exception:
                pass
            
            payload = None
            last_err = None
            for secret in secrets_to_try:
                try:
                    payload = jwt.decode(
                        token,
                        secret,
                        algorithms=["HS256"],
                        audience="authenticated"
                    )
                    break
                except jwt.InvalidSignatureError as e:
                    last_err = e
                    continue
                except jwt.InvalidTokenError as e:
                    raise e
            
            if payload:
                return payload
            elif last_err:
                raise last_err
    except jwt.ExpiredSignatureError:
        print("verify_supabase_jwt: Token signature has expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"verify_supabase_jwt: Invalid token error during HS256 decode: {str(e)}. Will try Supabase API fallback.")
    except Exception as e:
        print(f"verify_supabase_jwt: HS256 decode failed: {str(e)}. Will try Supabase API fallback.")

    # 3. Fallback: Supabase Auth API verification (supports ES256/RS256, etc.)
    try:
        if supabase:
            print("verify_supabase_jwt: Attempting Supabase Auth API token validation fallback...")
            user_resp = supabase.auth.get_user(token)
            if user_resp and user_resp.user:
                db_user = user_resp.user
                return {
                    "sub": db_user.id,
                    "email": db_user.email,
                    "user_metadata": db_user.user_metadata or {},
                    "created_at": db_user.created_at.isoformat() if db_user.created_at else None
                }
    except Exception as e:
        print(f"verify_supabase_jwt: Supabase API validation failed: {str(e)}")
        
    return None

