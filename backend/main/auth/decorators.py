from .. import jwt 
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] != 'admin':
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    claims = {
        'role': user.role,
        'email': user.email,
        'id': user.id,
    }
    return claims