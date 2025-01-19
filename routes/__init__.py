from .user_routes import user_bp
from .session_routes import session_bp

def init_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(session_bp)