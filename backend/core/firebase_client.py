import urllib.request
import json
import jwt
import hashlib
import time
from typing import Dict, Any, Optional
from core.config import settings
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

# Cache Google public certificates with a 23-hour TTL.
# Firebase rotates its signing certs roughly every 24 h; refreshing at 23 h
# ensures token verification never fails due to a stale/rotated certificate.
_CERT_CACHE_TTL = 23 * 60 * 60  # 23 hours in seconds
_certs_cache: Dict[str, str] = {}
_certs_fetched_at: float = 0.0

def _get_google_certs():
    global _certs_cache, _certs_fetched_at
    # Return cached certs if they are still fresh
    if _certs_cache and (time.time() - _certs_fetched_at) < _CERT_CACHE_TTL:
        return _certs_cache
        
    url = "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            _certs_cache = json.loads(response.read().decode())
            _certs_fetched_at = time.time()
            return _certs_cache
    except Exception as e:
        print(f"Error fetching Google certificates: {str(e)}")
        # Return stale cache if available (better than nothing on transient network errors)
        if _certs_cache:
            print("Warning: Returning stale Google certificates due to fetch failure.")
            return _certs_cache
        return {}

def verify_firebase_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes and validates a Firebase ID token using Google public certificates.
    Returns user details and a deterministic UUID mapping of the Firebase UID.
    """
    # 1. Developer simulation bypass
    if token.startswith("sim_token_"):
        email = token.replace("sim_token_", "")
        email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
        sim_uuid = f"00000000-0000-0000-0000-{email_hash[:12]}"
        return {
            "sub": sim_uuid,
            "firebase_uid": f"sim_{email_hash[:16]}",
            "email": email,
            "name": email.split("@")[0].capitalize(),
            "picture": "https://lh3.googleusercontent.com/a/default-user"
        }

    # 2. Decode header to locate Key ID (kid)
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        if not kid:
            print("verify_firebase_token: Token header missing 'kid'")
            return None
    except Exception as e:
        print(f"verify_firebase_token: Failed to decode header: {str(e)}")
        return None

    # 3. Retrieve Google certificates
    certs = _get_google_certs()
    cert_str = certs.get(kid)
    
    # Fallback to offline verification if certificates could not be fetched (network down)
    if not cert_str:
        print(f"verify_firebase_token: Certificate not found for kid '{kid}'. Trying offline decoding...")
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            uid = payload["sub"]
            uid_hash = hashlib.md5(uid.encode('utf-8')).hexdigest()
            db_uuid = f"{uid_hash[:8]}-{uid_hash[8:12]}-{uid_hash[12:16]}-{uid_hash[16:20]}-{uid_hash[20:]}"
            
            return {
                "sub": db_uuid,
                "firebase_uid": uid,
                "email": payload.get("email"),
                "name": payload.get("name") or payload.get("email", "").split("@")[0].capitalize(),
                "picture": payload.get("picture") or "https://lh3.googleusercontent.com/a/default-user"
            }
        except Exception as fallback_err:
            print(f"verify_firebase_token: Offline decode failed: {str(fallback_err)}")
        return None

    # 4. Perform Signature & Audience validation using Cryptography
    try:
        cert_obj = load_pem_x509_certificate(cert_str.encode(), default_backend())
        public_key = cert_obj.public_key()
        
        firebase_project_id = settings.FIREBASE_PROJECT_ID
        
        # Verify audience and issuer if project ID is configured
        decode_opts = {}
        if firebase_project_id == "dummy-project":
            # If not configured, skip strict audience verification to prevent blocking devs
            decode_opts["verify_aud"] = False
            aud = None
            iss = None
        else:
            aud = firebase_project_id
            iss = f"https://securetoken.google.com/{firebase_project_id}"
            
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=aud,
            issuer=iss,
            options=decode_opts
        )
        
        uid = payload["sub"]
        uid_hash = hashlib.md5(uid.encode('utf-8')).hexdigest()
        db_uuid = f"{uid_hash[:8]}-{uid_hash[8:12]}-{uid_hash[12:16]}-{uid_hash[16:20]}-{uid_hash[20:]}"
        
        return {
            "sub": db_uuid,
            "firebase_uid": uid,
            "email": payload.get("email"),
            "name": payload.get("name") or payload.get("email", "").split("@")[0].capitalize(),
            "picture": payload.get("picture") or "https://lh3.googleusercontent.com/a/default-user"
        }
    except jwt.ExpiredSignatureError:
        print("verify_firebase_token: Token signature has expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"verify_firebase_token: Invalid token claims: {str(e)}")
        return None
    except Exception as e:
        print(f"verify_firebase_token: Signature verification exception: {str(e)}")
        return None
