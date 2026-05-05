TEAM_MEMBERS = {
    "yhpang@oneboxagency.com": {"name": "yhpunk", "auto_pulse_tasks": True},
    "yhpunk@oneboxagency.com": {"name": "yhpunk", "auto_pulse_tasks": True},
}


def resolve_by_email(email: str) -> dict | None:
    return TEAM_MEMBERS.get(email.lower().strip()) if email else None


def resolve_by_name(name: str) -> dict | None:
    if not name:
        return None
    needle = name.lower().strip()
    for member in TEAM_MEMBERS.values():
        if member["name"].lower() == needle:
            return member
    return None


def is_team_email(email: str) -> bool:
    return resolve_by_email(email) is not None
