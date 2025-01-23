from app.models.task import Task
from app.models.goal import Goal
from app.extensions import db

def calculate_goal_progress(goal_id):
    """
    Calculate the percentage of completed tasks under a specific goal.
    """
    total_tasks = Task.query.filter_by(goal_id=goal_id).count()
    if total_tasks == 0:
        return 0  # Avoid division by zero; no progress if no tasks exist.
    
    completed_tasks = Task.query.filter_by(goal_id=goal_id, completed=True).count()
    progress_percentage = (completed_tasks / total_tasks) * 100
    return round(progress_percentage, 2)


def calculate_overall_progress(user_id):
    """
    Calculate the overall goal completion percentage for a user.
    """
    total_goals = Goal.query.filter_by(user_id=user_id).count()
    if total_goals == 0:
        return 0  # Avoid division by zero; no progress if no goals exist.
    
    completed_goals = Goal.query.filter_by(user_id=user_id, completed=True).count()
    overall_progress = (completed_goals / total_goals) * 100
    return round(overall_progress, 2)

