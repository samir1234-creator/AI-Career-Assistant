import os
import hmac
import hashlib
import base64
import json
import time
from typing import Dict, Any, Optional

JWT_SECRET = os.environ.get("JWT_SECRET", "super_secret_career_assistant_token_key_1234567890!")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_SECONDS = 7 * 24 * 60 * 60 # 7 days session persistence

def base64url_encode(data: bytes) -> str:
    encoded = base64.urlsafe_b64encode(data).decode('utf-8')
    return encoded.rstrip('=')

def base64url_decode(data: str) -> bytes:
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def encode_jwt(payload: Dict[str, Any]) -> str:
    """Signs and encodes a JWT token with the secret key."""
    # Add issue time and expiry if not present
    now = int(time.time())
    full_payload = payload.copy()
    if "iat" not in full_payload:
        full_payload["iat"] = now
    if "exp" not in full_payload:
        full_payload["exp"] = now + TOKEN_EXPIRY_SECONDS
        
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    
    header_bytes = json.dumps(header, sort_keys=True).encode('utf-8')
    payload_bytes = json.dumps(full_payload, sort_keys=True).encode('utf-8')
    
    header_b64 = base64url_encode(header_bytes)
    payload_b64 = base64url_encode(payload_bytes)
    
    signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    
    signature = hmac.new(
        JWT_SECRET.encode('utf-8'),
        signing_input,
        hashlib.sha256
    ).digest()
    
    signature_b64 = base64url_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def decode_jwt(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and validates a JWT token signature and expiry. Returns payload or None."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
            
        header_b64, payload_b64, signature_b64 = parts
        
        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        
        expected_signature = hmac.new(
            JWT_SECRET.encode('utf-8'),
            signing_input,
            hashlib.sha256
        ).digest()
        
        expected_signature_b64 = base64url_encode(expected_signature)
        
        # Verify signature securely
        if not hmac.compare_digest(signature_b64, expected_signature_b64):
            return None
            
        payload_bytes = base64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode('utf-8'))
        
        # Check expiry
        now = int(time.time())
        if "exp" in payload and payload["exp"] < now:
            return None # Expired
            
        return payload
    except Exception:
        return None
