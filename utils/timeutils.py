from datetime import datetime, timedelta

def monday_of_week(dt: datetime) -> datetime:
    # segunda-feira = 0
    return dt - timedelta(days=(dt.weekday()))

def iso_date(d: datetime) -> str:
    return d.strftime("%Y-%m-%d")
