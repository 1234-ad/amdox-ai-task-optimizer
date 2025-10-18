"""
API Module
REST API endpoints for the application
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import routes
