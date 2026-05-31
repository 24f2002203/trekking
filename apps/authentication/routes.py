from flask import Blueprint 

blueprint = Blueprint(
    'authentication', 
    __name__, 
    url_prefix='/authentication'
)

@blueprint.route('/test')
def test_authentication(): 
    return {"message":"Authentication route is working"} 