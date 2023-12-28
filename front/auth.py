import jwt
from django.conf import settings
from datetime import datetime, timezone
from rest_framework.authentication import BaseAuthentication
from .models import CustomUser, Jwt
import logging
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError

logger = logging.getLogger(__name__)


class Authentication(BaseAuthentication):
    def authenticate_header(self, request):
        return 'Bearer'

    def authenticate(self, request):
        data = self.validate_request(request.headers)
        if not data:
            return None, None

        return self.get_user(data["user_id"]), None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except Exception:
            return None

    def validate_request(self, headers):
        authorization = headers.get("Authorization", None)
        if not authorization:
            return None
        token = headers["Authorization"][7:]
        decoded_data = Authentication.verify_token(token)

        if not decoded_data:
            return None

        return decoded_data

    @staticmethod
    def verify_token(token):
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except DecodeError:
            logger.error("Error decoding token - DecodeError. Token: " + str(token))
            return None
        except InvalidTokenError:
            logger.error("Invalid token")
            return None
        except Exception as e:
            logger.error(f"Unexpected error decoding token: {e}")
            return None

        try:
            exp = decoded_data["exp"]
            if not exp:
                logger.warning(f'Nothing found in exp:\nexp: {exp}')
        except Exception as e:
            logger.warning(f'Error during founding exp: {e}')

        time = datetime.now(timezone.utc).timestamp()
        if time > exp:
            logger.warning(f'Token expired\n\nnow: {time}\nexp: {exp}')
            return None

        return decoded_data