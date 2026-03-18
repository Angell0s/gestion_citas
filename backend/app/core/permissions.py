# backend\app\core\permissions.py
from enum import Enum

class SystemPermissions(Enum):
    MANAGE_BUSINESS = "manage_business"
    MANAGE_EMPLOYEES = "manage_employees"
    MANAGE_ROLES = "manage_roles"

    MANAGE_SERVICES = "manage_services"

    VIEW_APPOINTMENTS = "view_appointments"
    MANAGE_APPOINTMENTS = "manage_appointments"
    CONFIRM_APPOINTMENTS = "confirm_appointments"
    CANCEL_APPOINTMENTS = "cancel_appointments"

    VIEW_CLIENTS = "view_clients"
    MANAGE_CLIENTS = "manage_clients"

    VIEW_REPORTS = "view_reports"