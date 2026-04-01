from datetime import datetime, timedelta


def round_to_nearest_date_at_midnight(dt:datetime):
    return (dt+ timedelta(hours=12)).replace(hour=0, minute=0, second=0, microsecond=0)