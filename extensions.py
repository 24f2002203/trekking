from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_security import Security

'''limiter = Limiter( #setting up the limiter 
        get_remote_address, 
        storage_uri = "memory://"
    )'''

security = Security()

