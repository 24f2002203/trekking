from flask import Blueprint 

blueprint = Blueprint(
    'user', 
    __name__, 
    url_prefix='/user'
)

@blueprint.route('/test')
def test_user(): 
    return {"message":"User route is working"} 