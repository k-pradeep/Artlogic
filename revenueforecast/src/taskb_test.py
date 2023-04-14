from datetime import datetime, timedelta

def get_grace_period(schedule_due_date, schedule_due_date_type):
    """Generates time period between schedule date date and due date

    Args:
        schedule_due_date (str): number of days before invoice is due
        schedule_due_date_type (str): provides due date type either before or after

    Returns:
        grace_period (datetime): number of days to be added
    """
    grace_period = None

    if schedule_due_date_type == "DAYSAFTERBILLDATE":
        # this holds time interval between schedule date and due date.
        grace_period = timedelta(int(schedule_due_date))

    return grace_period

result = get_grace_period('7','DAYSAFTERBILLDATE')
print(result)
