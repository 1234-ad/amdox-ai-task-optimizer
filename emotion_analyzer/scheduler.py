"""
Emotion Analysis Scheduler
Schedules and manages periodic emotion analysis tasks
"""

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from typing import Callable, Dict

logger = logging.getLogger(__name__)

class EmotionAnalysisScheduler:
    """Manages scheduled emotion analysis tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}
        logger.info("Emotion analysis scheduler initialized")
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Emotion analysis scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Emotion analysis scheduler stopped")
    
    def schedule_daily_analysis(self, func: Callable, hour: int = 9, minute: int = 0):
        """Schedule daily emotion analysis"""
        job_id = 'daily_analysis'
        
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
        
        job = self.scheduler.add_job(
            func,
            CronTrigger(hour=hour, minute=minute),
            id=job_id,
            name='Daily Emotion Analysis',
            replace_existing=True
        )
        
        self.jobs[job_id] = job
        logger.info(f"Scheduled daily analysis at {hour}:{minute:02d}")
    
    def schedule_weekly_report(self, func: Callable, day_of_week: int = 0, hour: int = 10):
        """Schedule weekly emotion report generation"""
        job_id = 'weekly_report'
        
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
        
        job = self.scheduler.add_job(
            func,
            CronTrigger(day_of_week=day_of_week, hour=hour),
            id=job_id,
            name='Weekly Emotion Report',
            replace_existing=True
        )
        
        self.jobs[job_id] = job
        logger.info(f"Scheduled weekly report on day {day_of_week} at {hour}:00")
    
    def schedule_hourly_monitoring(self, func: Callable):
        """Schedule hourly stress monitoring"""
        job_id = 'hourly_monitoring'
        
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
        
        job = self.scheduler.add_job(
            func,
            'interval',
            hours=1,
            id=job_id,
            name='Hourly Stress Monitoring',
            replace_existing=True
        )
        
        self.jobs[job_id] = job
        logger.info("Scheduled hourly stress monitoring")
    
    def schedule_custom_interval(self, func: Callable, minutes: int, job_id: str):
        """Schedule custom interval task"""
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
        
        job = self.scheduler.add_job(
            func,
            'interval',
            minutes=minutes,
            id=job_id,
            replace_existing=True
        )
        
        self.jobs[job_id] = job
        logger.info(f"Scheduled {job_id} every {minutes} minutes")
    
    def remove_job(self, job_id: str):
        """Remove a scheduled job"""
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]
            logger.info(f"Removed job: {job_id}")
    
    def get_jobs(self) -> Dict:
        """Get all scheduled jobs"""
        return {
            job_id: {
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            }
            for job_id, job in self.jobs.items()
        }

# Global scheduler instance
_scheduler = None

def get_scheduler() -> EmotionAnalysisScheduler:
    """Get or create global scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = EmotionAnalysisScheduler()
    return _scheduler

def start_emotion_analysis_scheduler():
    """Start the global emotion analysis scheduler"""
    scheduler = get_scheduler()
    
    # Schedule default tasks
    # Add your default scheduled tasks here
    
    scheduler.start()
    logger.info("Started emotion analysis scheduler with default tasks")
    
    return scheduler
