from importlib import import_module 


def register_blueprints(app): 
    for module_name in ('authentication', 'staff', 'user', 'admin'): 
        module = import_module(f'apps.{module_name}.routes')
        
        app.register_blueprint(module.blueprint)