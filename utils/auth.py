from flask import request, g, jsonify
from jose import jwt, JWTError, ExpiredSignatureError
from functools import wraps
from urllib.request import urlopen
import json
import os

# Auth0 Configuration - replace with your values
AUTH0_DOMAIN = 'dev-pw44rpbvw3tnafw7.us.auth0.com'
API_AUDIENCE = 'https://dev-pw44rpbvw3tnafw7.us.auth0.com/api/v2/'
#API_AUDIENCE = 'jVGsdmyz2AzNGdpsbTkcETnU7oJVtuWp'
ALGORITHMS = ["RS256"]

# Auth Error Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Auth Header
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description": "Authorization header is expected"}, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({"code": "invalid_header",
                        "description": "Authorization header must start with Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description": "Authorization header must be Bearer token"}, 401)

    token = parts[1]
    return token

# Check Permissions
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({"code": "invalid_claims",
                        "description": "Permissions not included in JWT"}, 400)
    if permission not in payload['permissions']:
        raise AuthError({"code": "unauthorized",
                        "description": "Permission not found"}, 403)
    return True
# Verify JWT
def verify_decode_jwt(token):
    """Decodes the JWT Token"""
    try:
        jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        claims = jwt.get_unverified_claims(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
            namespace = 'https://anotherdsp.com/claims' # Must match the namespace in the Auth0 Rule
            app_metadata = payload.get(namespace + 'app_metadata', {}) 
            print(claims)
            print(app_metadata)
            return payload, app_metadata  # Return both payload and app_metadata  
        raise AuthError({"code": "token_expired", "description": "Token expired"}, 401)
    except JWTError as e:
        # Catching JWTError for other JWT related issues
        raise AuthError({"code": "jwt_error", "description": "JWT Error: " + str(e)}, 400)
    except Exception as e:
        # Catching general exceptions
        raise AuthError({"code": "invalid_token", "description": "Invalid token: " + str(e)}, 400)

    raise AuthError({"code": "invalid_header", "description": "Unable to find the appropriate key"}, 400)

# Requires Auth Decorator
def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Your authentication logic here...
        # For example, getting and verifying the token
        try:
            token = get_token_auth_header()
            payload, app_metadata = verify_decode_jwt(token)
            if 'buyer_id' in app_metadata:
                buyer_id = app_metadata['buyer_id']
                kwargs['buyer_id'] = buyer_id  
        except AuthError as auth_error:
            # Handle authentication errors
            return handle_auth_error(auth_error)

        return f(*args, **kwargs)
    return decorated_function

# Error Handling
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
