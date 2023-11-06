def seconds_to_largest_time_unit(seconds):
    """Function to turn unix difference into amount of time remaining"""

    # If time is negative then, return 0 seconds
    if seconds <= 0:
        return "0 seconds"

    # Convert total seconds to days
    days = seconds // 86400

    # If there are one or more days, return the days with the correct plurality
    if days > 0:
        return f"{days} day{'s' if days != 1 else ''}"

    # If there are no days, convert the remaining seconds to hours
    hours = (seconds // 3600) % 24

    # If there are one or more hours, return the hours with the correct
    # plurality
    if hours > 0:
        return f"{hours} hour{'s' if hours != 1 else ''}"

    # If there are no hours, convert the remaining seconds to minutes
    minutes = (seconds // 60) % 60

    # If there are one or more minutes, return the minutes with the correct
    # plurality
    if minutes > 0:
        return f"{minutes} minute{'s' if minutes != 1 else ''}"

    # If there are no minutes, just return the remaining seconds with the
    # correct plurality
    seconds = seconds % 60
    return f"{seconds} second{'s' if seconds != 1 else ''}"
