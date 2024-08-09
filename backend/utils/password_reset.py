import os
from itsdangerous import URLSafeTimedSerializer
from config.config import SECRET_KEY

SALT = "gensalt"


# generate password reset token function
def generate_password_reset_token(email):
    serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    return serializer.dumps(email, salt=SALT)


# verify password reset token function
def verify_password_reset_token(token, expires=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt= SALT,
            max_age=expires
        )
    except:
        return False
    return email    