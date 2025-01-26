from flask_apscheduler import APScheduler
from app.routes.email import send_task_reminders, send_goal_deadline_reminders

scheduler = APScheduler()

def configure_scheduler(app):
    scheduler.init_app(app)

    # Schedule task reminders every day at 8 AM
    scheduler.add_job(
        id="task_reminders",
        func=send_task_reminders,
        trigger="cron",
        hour=8,
        minute=0,
    )

    # Schedule goal deadline reminders every day at 9 AM
    scheduler.add_job(
        id="goal_deadline_reminders",
        func=send_goal_deadline_reminders,
        trigger="cron",
        hour=9,
        minute=0,
    )

    scheduler.start()

