# Imports
from utils.pfa.male.male_score_a import MaleScoreA
from datetime import datetime


def _seconds(time_str: str) -> int:
    """Function to turn time in `mm:ss` format to integer seconds"""

    # Parse the time
    time_obj = datetime.strptime(time_str, "%M:%S")

    # Convert to seconds
    total_seconds = time_obj.minute * 60 + time_obj.second

    # Return total seconds
    return total_seconds


def _in_range(range_str_map: dict, run_time: str) -> float:
    """Function to return the run subscore from given run time"""

    # Iterate through each key
    for i in range_str_map:
        # Continue if the value of the iterated key is 60
        if range_str_map[i] == 60:
            continue

        # Get the range of the iterate key
        time_range = []
        for j in i.split("-"):
            time_range.append(_seconds(j.strip()))

        # Return value if the given run_time_str is in range
        if run_time >= time_range[0] and run_time <= time_range[1]:
            # Return
            return range_str_map[i]

    # Return 0 if not in range
    return 0


def calculate_pfa(
    gender: str, age: int, pushups: int, situps: int, run_time: str
) -> float:
    """Function to give path to file that contains the correct score specs"""

    # Get the dictionary mappings
    pushup_map = {}
    situp_map = {}
    run_map = {}

    #
    #   MAPPING
    #

    # Map for males
    if gender == "male":
        # Map for males less than 25 years
        if age < 25:
            pushup_map = MaleScoreA.pushup_map
            situp_map = MaleScoreA.situp_map
            run_map = MaleScoreA.run_map

    # Variable declaration
    composite = 0
    run_time = _seconds(run_time)
    pushup_keys = list(pushup_map.keys())
    situp_keys = list(situp_map.keys())
    run_keys = list(run_map.keys())

    #
    #   PUSHUP CALCULATIONS
    #

    if pushups < pushup_keys[-1]:
        pass
    elif pushups >= pushup_keys[0]:
        composite += 20
    else:
        composite += pushup_map[pushups]

    #
    #   SITUP CALCULATIONS
    #

    if situps < situp_keys[-1]:
        pass
    elif situps >= situp_keys[0]:
        composite += 20
    else:
        composite += situp_map[situps]

    #
    #   RUN CALCULATIONS
    #

    if run_time <= _seconds(run_keys[0]):
        composite += 60
    else:
        composite += _in_range(run_map, run_time)

    # Return composite
    return composite
