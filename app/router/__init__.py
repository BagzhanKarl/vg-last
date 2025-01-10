from app.router.admin import admin
from app.router.webhook import webhook_bp

def register_routers(app):
    app.register_blueprint(admin)
    app.register_blueprint(webhook_bp)