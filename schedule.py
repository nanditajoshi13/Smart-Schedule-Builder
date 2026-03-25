from dataclasses import dataclass, field
from typing import Literal
from math import ceil


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

def _score(task: Task) -> float:
    urgency = 1.0 / max(task.deadline_in, 0.1)
    return urgency * TASK_WEIGHT[task.task_type] * task.priority


def _parse_time(t: str) -> float:
    """Convert '17' or '17:00' → 17.0"""
    try:
        if ":" in t:
            h, m = t.split(":")
            return float(h) + float(m) / 60
        return float(t)
    except:
        return 0.0


def _parse_range(range_str: str):
    """Convert '9-17' or '9:00-17:00' → (9.0, 17.0)"""
    try:
        start, end = range_str.split("-")
        return _parse_time(start), _parse_time(end)
    except:
        return 9.0, 17.0  # fallback


def _parse_breaks(break_str: str):
    """Convert '15min/every 1hr' → (interval, duration)"""
    try:
        part1, part2 = break_str.split("/every ")

        if "min" in part1:
            duration = float(part1.replace("min", "")) / 60
        else:
            duration = float(part1.replace("hr", ""))

        if "min" in part2:
            interval = float(part2.replace("min", "")) / 60
        else:
            interval = float(part2.replace("hr", ""))

        return interval, duration
    except:
        return 1.0, 0.25  


def _fmt(hour: float) -> str:
    h = int(hour)
    m = int((hour - h) * 60)
    return f"{h:02d}:{m:02d}"


def create_profile_from_db(user: dict):

    work_start, work_end = _parse_range(user.get("work_hours", "9-17"))


    unavailable = []
    if user.get("no_way"):
        no_start, no_end = _parse_range(user["no_way"])
        unavailable.append((no_start, no_end))

    break_interval, break_duration = _parse_breaks(
        user.get("breaks", "15min/every 1hr")
    )

    style = (user.get("style") or "flexible").lower()
    if style not in ["fixed", "flexible"]:
        style = "flexible"

    return UserProfile(
        work_start=work_start,
        work_end=work_end,
        unavailable=unavailable,
        schedule_type=style,
        break_interval=break_interval,
        break_duration=break_duration
    )

def build_schedule(profile: UserProfile, tasks: list[Task]):

    hard_end = profile.work_end + profile.extra_hours
    res = profile.slot_resolution

    sorted_tasks = sorted(tasks, key=_score, reverse=True)
    remaining = {id(t): t.duration for t in sorted_tasks}

    schedule = []
    cursor = profile.work_start
    work_since = 0
    task_cursor = 0

    while cursor < hard_end:

        blocked = False
        for start, end in profile.unavailable:
            if start <= cursor < end:
                schedule.append({
                    "time": f"{_fmt(cursor)} - {_fmt(cursor + res)}",
                    "task": "Unavailable"
                })
                cursor += res
                work_since = 0
                blocked = True
                break

        if blocked:
            continue

        if profile.break_interval > 0 and work_since >= profile.break_interval:
            end = min(cursor + profile.break_duration, hard_end)
            schedule.append({
                "time": f"{_fmt(cursor)} - {_fmt(end)}",
                "task": "Break"
            })
            cursor = end
            work_since = 0
            continue

        assigned = False
        attempts = 0

        while attempts < len(sorted_tasks):
            idx = (task_cursor + attempts) % len(sorted_tasks)
            task = sorted_tasks[idx]
            rem = remaining[id(task)]

            if rem <= 0:
                attempts += 1
                continue

            max_chunk = task.chunk_size if profile.schedule_type == "flexible" else rem
            chunk = min(rem, max_chunk, hard_end - cursor)
            chunk = ceil(chunk / res) * res

            end_time = cursor + chunk

            schedule.append({
                "time": f"{_fmt(cursor)} - {_fmt(end_time)}",
                "task": task.name
            })

            remaining[id(task)] -= chunk
            cursor = end_time
            work_since += chunk

            if profile.schedule_type == "flexible":
                task_cursor = (idx + 1) % len(sorted_tasks)

            assigned = True
            break

        if not assigned:
            break

    return {"schedule": schedule}
