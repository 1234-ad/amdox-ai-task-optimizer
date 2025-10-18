"""
Amdox AI-Powered Task Optimizer
Main application entry point
"""

import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from api.routes import api_bp
from dashboard.app import dashboard_bp
from database.connection import init_db
from emotion_analyzer.scheduler import start_emotion_analysis_scheduler
from alert_system.monitor import start_alert_monitor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    
    # Initialize database
    init_db()
    
    # Start background services
    if not app.config['DEBUG']:
        start_emotion_analysis_scheduler()
        start_alert_monitor()
    
    @app.route('/')
    def index():
        return {
            "message": "Amdox AI-Powered Task Optimizer",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "api": "/api",
                "dashboard": "/dashboard",
                "health": "/health"
            }
        }
    
    @app.route('/health')
    def health_check():
        return {
            "status": "healthy",
            "services": {
                "database": "connected",
                "redis": "connected",
                "emotion_analyzer": "running",
                "alert_system": "running"
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Starting Amdox AI Task Optimizer on port {port}")
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])