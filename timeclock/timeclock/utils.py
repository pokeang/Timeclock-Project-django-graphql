from datetime import datetime, timedelta
from graphql_jwt.settings import jwt_settings
    
## JWT payload for Hasura
def jwt_payload(user, context=None):
    jwt_datetime = datetime.now() + jwt_settings.JWT_EXPIRATION_DELTA
    jwt_expires = int(jwt_datetime.timestamp())
    payload = {}
    payload['username'] = str(user.username) # For library compatibility
    payload['sub'] = str(user.id)
    payload['sub_email'] = user.email
    payload['exp'] = jwt_expires
    return payload
