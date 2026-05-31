from flask import Blueprint 

blueprint = Blueprint(
    'admin', 
    __name__, 
    url_prefix='/admin'
)

@blueprint.route('/test')
def test_admin(): 
    return {"message":"Admin route is working"} 