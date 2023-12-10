import json
from datetime import datetime


def BigAvailabiltyData(data: list):
    big_data = {}
    for item in data:
        item_data = json.loads(item["availablilityData"])
        if item_data:
            for availablility in item_data:
                day = availablility.pop(0)
                if day not in big_data:
                    big_data.update(
                        {
                            day: [
                                availablility,
                            ]
                        }
                    )
                else:
                    big_data[day].append(availablility)
    return big_data


def NewAvailaibilityData(data_str: str):
    new_data = {}
    data = json.loads(data_str)
    for availablility in data:
        day = availablility.pop(0)
        if day not in new_data:
            new_data.update(
                {
                    day: [
                        availablility,
                    ]
                }
            )
        else:
            new_data[day].append(availablility)

    return new_data


def checkConflict(
    old_data: dict, new_data: dict, against: bool
):  # against takes a boolean parameter so you know if you're comparing new data against or with the new data
    common_days = list(set(old_data.keys()) & set(new_data.keys()))
    conflicts = {}
    for day in common_days:
        existing_day = old_data[day]
        new_day = new_data[day]
        for time_range in existing_day:
            old_from, old_to = [
                datetime.strptime(time_range[0], "%H:%M").time(),
                datetime.strptime(time_range[1], "%H:%M").time(),
            ]

            for time_range in new_day:
                new_from, new_to = [
                    datetime.strptime(time_range[0], "%H:%M").time(),
                    datetime.strptime(time_range[1], "%H:%M").time(),
                ]

            if against:
                if old_from <= new_from <= old_to:
                    print("There is no conflict on", day)
                else:
                    conflicts = {day: time_range}
                    return conflicts
            else:
                if old_from <= new_from <= old_to:
                    conflicts = {day: time_range}
                    return conflicts
                else:
                    print("There is no conflict on", day)
