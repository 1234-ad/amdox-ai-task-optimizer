"""
Dashboard Module
Web-based analytics dashboard
"""

from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

from . import app
