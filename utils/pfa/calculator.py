# Imports
from datetime import datetime
from utils.pfa.male import (
    MaleScoreA,
    MaleScoreB,
    MaleScoreC,
    MaleScoreD,
    MaleScoreE,
    MaleScoreF,
    MaleScoreG,
    MaleScoreH,
    MaleScoreI,
)
from utils.pfa.female import (
    FemaleScoreA,
    FemaleScoreB,
    FemaleScoreC,
    FemaleScoreD,
    FemaleScoreE,
    FemaleScoreF,
    FemaleScoreG,
    FemaleScoreH,
    FemaleScoreI,
)


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
        if age < 25:
            pushup_map = MaleScoreA.pushup_map
            situp_map = MaleScoreA.situp_map
            run_map = MaleScoreA.run_map
        elif age >= 25 and age <= 29:
            pushup_map = MaleScoreB.pushup_map
            situp_map = MaleScoreB.situp_map
            run_map = MaleScoreB.run_map
        elif age >= 30 and age <= 34:
            pushup_map = MaleScoreC.pushup_map
            situp_map = MaleScoreC.situp_map
            run_map = MaleScoreC.run_map
        elif age >= 35 and age <= 39:
            pushup_map = MaleScoreD.pushup_map
            situp_map = MaleScoreD.situp_map
            run_map = MaleScoreD.run_map
        elif age >= 40 and age <= 44:
            pushup_map = MaleScoreE.pushup_map
            situp_map = MaleScoreE.situp_map
            run_map = MaleScoreE.run_map
        elif age >= 45 and age <= 49:
            pushup_map = MaleScoreF.pushup_map
            situp_map = MaleScoreF.situp_map
            run_map = MaleScoreF.run_map
        elif age >= 50 and age <= 54:
            pushup_map = MaleScoreG.pushup_map
            situp_map = MaleScoreG.situp_map
            run_map = MaleScoreG.run_map
        elif age >= 55 and age <= 59:
            pushup_map = MaleScoreH.pushup_map
            situp_map = MaleScoreH.situp_map
            run_map = MaleScoreH.run_map
        elif age >= 60:
            pushup_map = MaleScoreI.pushup_map
            situp_map = MaleScoreI.situp_map
            run_map = MaleScoreI.run_map
    elif gender == "female":
        if age < 25:
            pushup_map = FemaleScoreA.pushup_map
            situp_map = FemaleScoreA.situp_map
            run_map = FemaleScoreA.run_map
        elif age >= 25 and age <= 29:
            pushup_map = FemaleScoreB.pushup_map
            situp_map = FemaleScoreB.situp_map
            run_map = FemaleScoreB.run_map
        elif age >= 30 and age <= 34:
            pushup_map = FemaleScoreC.pushup_map
            situp_map = FemaleScoreC.situp_map
            run_map = FemaleScoreC.run_map
        elif age >= 35 and age <= 39:
            pushup_map = FemaleScoreD.pushup_map
            situp_map = FemaleScoreD.situp_map
            run_map = FemaleScoreD.run_map
        elif age >= 40 and age <= 44:
            pushup_map = FemaleScoreE.pushup_map
            situp_map = FemaleScoreE.situp_map
            run_map = FemaleScoreE.run_map
        elif age >= 45 and age <= 49:
            pushup_map = FemaleScoreF.pushup_map
            situp_map = FemaleScoreF.situp_map
            run_map = FemaleScoreF.run_map
        elif age >= 50 and age <= 54:
            pushup_map = FemaleScoreG.pushup_map
            situp_map = FemaleScoreG.situp_map
            run_map = FemaleScoreG.run_map
        elif age >= 55 and age <= 59:
            pushup_map = FemaleScoreH.pushup_map
            situp_map = FemaleScoreH.situp_map
            run_map = FemaleScoreH.run_map
        elif age >= 60:
            pushup_map = FemaleScoreI.pushup_map
            situp_map = FemaleScoreI.situp_map
            run_map = FemaleScoreI.run_map
    else:
        return -1

    # Variable declaration
    composite = 0
    run_time = _seconds(run_time)
    pushup_keys = list(pushup_map.keys())
    situp_keys = list(situp_map.keys())
    run_keys = list(run_map.keys())

    #
    #   PUSHUP CALCULATIONS
    #

    if pushups < int(pushup_keys[-1]):
        pass
    elif pushups >= int(pushup_keys[0]):
        composite += 20
    else:
        composite += pushup_map[str(pushups)]

    #
    #   SITUP CALCULATIONS
    #

    if situps < int(situp_keys[-1]):
        pass
    elif situps >= int(situp_keys[0]):
        composite += 20
    else:
        composite += situp_map[str(situps)]

    #
    #   RUN CALCULATIONS
    #

    if run_time <= _seconds(run_keys[0]):
        composite += 60
    else:
        composite += _in_range(run_map, run_time)

    # Return composite
    return composite
