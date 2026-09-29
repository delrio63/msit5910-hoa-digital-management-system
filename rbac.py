def can_view_board_dashboard(role):
    return role in ["admin", "board_member"]


def can_view_resident_portal(role):
    return role in ["admin", "resident"]


def is_admin(role):
    return role == "admin"
