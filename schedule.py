from dataclasses import dataclass, field
from typing import Literal
from datetime import datetime, timedelta

ScheduleType = Literal["fixed", "flexible"]
TaskType     = Literal["exam_prep", "assignment", "project", "housework", "other"]

TASK_WEIGHT = {
    "exam_prep":  1.5,
    "assignment": 1.3,
    "project":    1.2,
    "housework":  1.0,
    "other":      1.0,
}

@dataclass
class Task:
    name: str
    duration: float
    task_type: TaskType = "other"
    priority: int = 3
    deadline_in: float = 999
    chunk_size: float = 1.0


@dataclass
class UserProfile:
    work_start: float
    work_end: float
    extra_hours: float = 0.0
    unavailable: list[tuple[float, float]] = field(default_factory=list)
    schedule_type: ScheduleType = "flexible"
    break_interval: float = 1.0
    break_duration: float = 0.25
    slot_resolution: float = 0.25

def _parse_time(t: str) -> float:
    try:
        if ":" in t:
            h, m = t.split(":")
            return float(h) + float(m) / 60
        return float(t)
    except:
        return 9.0

def _parse_range(range_str):
    try:
        start, end = range_str.split("-")
        return _parse_time(start), _parse_time(end)
    except:
        return 9.0, 17.0

def _parse_breaks(break_str):
    try:
        part1, part2 = break_str.split("/every ")

        duration = float(part1.replace("min", "").replace("hr", ""))
        if "min" in part1:
            duration /= 60

        interval = float(part2.replace("min", "").replace("hr", ""))
        if "min" in part2:
            interval /= 60

        return interval, duration
    except:
        return 1.0, 0.25  

def _fmt(hour):
    h = int(hour)
    m = int((hour - h) * 60)
    return f"{h:02d}:{m:02d}"

def _score(task: Task) -> float:
    urgency = 1 / max(task.deadline_in, 1)
    return urgency * TASK_WEIGHT[task.task_type] * task.priority

def create_profile_from_db(user: dict):

    work_start, work_end = _parse_range(user["work_hours"])

    unavailable = []
    if user.get("no_way"):
        no_start, no_end = _parse_range(user["no_way"])
        unavailable.append((no_start, no_end))

    break_interval, break_duration = _parse_breaks(user["breaks"])
 
    return UserProfile(
        work_start=work_start,
        work_end=work_end,
        unavailable=unavailable,
        schedule_type=(user.get("style") or "flexible"),
        break_interval=break_interval,
        break_duration=break_duration
    )

def build_schedule(profile: UserProfile, tasks: list[Task]):

    MAX_DAYS = 14

    sorted_tasks = sorted(tasks, key=_score, reverse=True)
    remaining = {id(t): t.duration for t in sorted_tasks}

    full_schedule = []
    today = datetime.now()

    for day_offset in range(MAX_DAYS):

        if all(v <= 0 for v in remaining.values()):
            break

        date = (today + timedelta(days=day_offset)).strftime("%Y-%m-%d")

        cursor = profile.work_start
        work_since = 0
        hard_end = profile.work_end

        day_schedule = []

        while cursor < hard_end:
            blocked = False
            for start, end in profile.unavailable:
                if start <= cursor < end:
                    cursor += profile.slot_resolution
                    work_since = 0
                    blocked = True
                    break
            if blocked:
                continue

            if work_since >= profile.break_interval:
                end = min(cursor + profile.break_duration, hard_end)
                day_schedule.append({
                    "time": f"{_fmt(cursor)} - {_fmt(end)}",
                    "task": "Break"
                })
                cursor = end
                work_since = 0
                continue

            assigned = False

            for task in sorted_tasks:
                if remaining[id(task)] <= 0:
                    continue
                chunk = min(
                    task.chunk_size,
                    remaining[id(task)],
                    hard_end - cursor
                )
                if chunk <= 0:
                    continue

                end_time = cursor + chunk

                day_schedule.append({
                    "time": f"{_fmt(cursor)} - {_fmt(end_time)}",
                    "task": task.name
                })

                remaining[id(task)]-= chunk
                cursor = end_time
                work_since += chunk

                assigned = True
                break

            if not assigned:
                break

        full_schedule.append({
            "date":date,
            "entries": day_schedule
        })

    if any(v > 0 for v in remaining.values()):
        full_schedule.append({
            "date": "Warning",
            "entries": [{"time": "", "task": "Not enough time to complete all tasks"}]
        })

    return {"schedule": full_schedule}
