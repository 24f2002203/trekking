from flask import Blueprint 

blueprint = Blueprint(
    'staff', 
    __name__, 
    url_prefix='/staff'
)

@blueprint.route('/test')
def test_staff(): 
    return {"message":"Staff route is working"} 