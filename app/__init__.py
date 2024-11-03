from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.core.celery_worker import  make_celery

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    from app.core.container import Container
    from app.core.config import AppConfig
    
    config = AppConfig.from_env()
    app.config.from_object(config)

    with app.app_context():
        container = Container(config=config, app=app)
        db.init_app(app)
        db.create_all()
        
    app.container = container
    
    celery = make_celery(app)
    celery.set_default()
    
    from app.api.routes import JobRoutes
    job_routes = JobRoutes(
        container.job_service,
        container.subscriber_service
    ).job_routes
    
    from app.common.decorators.error_handler import error_handlers
    app.register_blueprint(job_routes)
    app.register_blueprint(error_handlers)

    return app, celery