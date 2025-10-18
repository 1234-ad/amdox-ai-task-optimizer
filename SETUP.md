# Setup and Installation Guide

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12+ (optional, for production)
- Redis (optional, for caching and background tasks)
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/1234-ad/amdox-ai-task-optimizer.git
cd amdox-ai-task-optimizer
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Installation may take 10-15 minutes due to ML libraries.

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# For quick start, default values will work
```

### 5. Initialize Database (Optional)

For development, the app will work without a database. For production:

```bash
# Create PostgreSQL database
createdb amdox_task_optimizer

# Run migrations (if using Alembic)
alembic upgrade head
```

### 6. Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```

### 7. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Accessing the Application

- **Dashboard**: http://localhost:5000/dashboard
- **API Documentation**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/health

## Testing the API

### Test Text Emotion Analysis

```bash
curl -X POST http://localhost:5000/api/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text": "I am feeling great today and excited about the new project!"}'
```

### Test Task Recommendations

```bash
curl -X POST http://localhost:5000/api/tasks/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "employee_state": {
      "dominant_emotion": "happiness",
      "stress_assessment": {
        "overall_stress_score": 0.3,
        "burnout_risk": {"risk_level": "minimal"}
      }
    },
    "available_tasks": [
      {
        "task_id": "TASK001",
        "name": "Design dashboard",
        "category": "creative",
        "priority": "high",
        "complexity": "medium",
        "estimated_hours": 8
      }
    ],
    "limit": 5
  }'
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
cd deployment
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis cache
- Main application
- Celery workers
- Celery beat scheduler

### Using Docker Only

```bash
# Build image
docker build -t amdox-task-optimizer -f deployment/Dockerfile .

# Run container
docker run -p 5000:5000 \
  -e DATABASE_URL=your-db-url \
  -e SECRET_KEY=your-secret-key \
  amdox-task-optimizer
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code
black .

# Lint code
flake8 .
```

### Running in Debug Mode

```bash
# Set DEBUG=True in .env
python app.py
```

## Troubleshooting

### Issue: TensorFlow/PyTorch Installation Fails

**Solution**: Install CPU versions separately:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install tensorflow-cpu
```

### Issue: Database Connection Error

**Solution**: 
1. Check PostgreSQL is running
2. Verify DATABASE_URL in .env
3. The app can run without database for testing

### Issue: Model Download Slow

**Solution**: Models will download on first use. This is normal and only happens once.

### Issue: Port 5000 Already in Use

**Solution**: Change PORT in .env file or stop the conflicting service.

## Production Deployment

### Security Checklist

- [ ] Change SECRET_KEY in .env
- [ ] Set DEBUG=False
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up monitoring
- [ ] Enable email notifications
- [ ] Configure backup strategy
- [ ] Review CORS settings
- [ ] Enable API authentication

### Performance Optimization

1. **Use GPU for ML models** (if available)
   ```
   MODEL_DEVICE=cuda
   ENABLE_GPU=True
   ```

2. **Scale with multiple workers**
   ```bash
   gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
   ```

3. **Enable Redis caching**

4. **Use PostgreSQL for production**

5. **Set up load balancing** (Nginx, AWS ELB, etc.)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Amdox AI System                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Text      │  │   Facial     │  │   Speech     │  │
│  │  Analyzer   │  │  Analyzer    │  │  Analyzer    │  │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                │                  │           │
│         └────────────────┼──────────────────┘           │
│                          ↓                              │
│                 ┌────────────────┐                      │
│                 │ Emotion Fusion │                      │
│                 └────────┬───────┘                      │
│                          │                              │
│         ┌────────────────┼────────────────┐            │
│         ↓                ↓                ↓            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │    Task     │  │   Alert     │  │  Dashboard  │   │
│  │  Optimizer  │  │   System    │  │     UI      │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/1234-ad/amdox-ai-task-optimizer/issues
- Email: support@amdox.com
- Documentation: https://docs.amdox.com

## License

MIT License - see LICENSE file for details.
