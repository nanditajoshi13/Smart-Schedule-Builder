def build_schedule_round_robin(user_profile, tasks):
    schedule = []
    current_hour = 9
    total_hours = user_profile["work_hours"]

    task_index = 0

    while total_hours > 0 and tasks:
        task = tasks[task_index]
        duration = min(task["duration"], total_hours)

        schedule.append({
            "time": f"{current_hour}:00 - {current_hour + duration}:00",
            "task": task["name"]
        })

        current_hour += duration
        total_hours -= duration
        task_index = (task_index + 1) % len(tasks)

    return schedule
