# from datetime import datetime, timezone, timedelta
# import jwt
# from config import settings
#
#
# def create_access_token(user):
#     now = datetime.now(timezone.utc)
#
#     payload = {
#         'user_id': user.id,
#         'exp': int((now + timedelta(minutes=2)).timestamp()),
#         'cr_at': int((now.timestamp()))
#     }
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#     return token
#
#
# def create_refresh_token(user):
#     now = datetime.now(timezone.utc)
#
#     payload = {
#         'user_id': user.id,
#         'exp': int((now + timedelta(minutes=2)).timestamp()),
#         'cr_at': int((now.timestamp()))
#     }
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#     return token
#
#
# def decode_token(token):
#     return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
