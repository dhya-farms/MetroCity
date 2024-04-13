from enum import Enum


class Timeouts:
    SECONDS_10 = 10
    MINUTES_2 = 2 * 60
    MINUTES_10 = 10 * 60
    MINUTES_30 = 30 * 60
    HOUR_1 = 1 * 60 * 60
    HOUR_6 = 6 * 60 * 60
    HOUR_24 = 24 * 60 * 60
    DAY_5 = 5 * 24 * 60 * 60
    ONE_MONTH = 30 * 24 * 60 * 60


class CacheKeys(Enum):
    # LIST
    USER_LIST = None
    CUSTOMER_LIST = None
    PROPERTY_LIST = None
    PHASE_LIST = None
    PLOT_LIST = None
    CRM_LEAD_LIST = None
    STATUS_CHANGE_REQUEST_LIST = None
    PAYMENT_LIST = None
    SITE_VISIT_LIST = None

    # DETAILS
    USER_DETAILS_BY_PK = None
    CUSTOMER_DETAILS_BY_PK = None
    PROPERTY_DETAILS_BY_PK = None
    PHASE_DETAILS_BY_PK = None
    PLOT_DETAILS_BY_PK = None
    CRM_LEAD_DETAILS_BY_PK = None
    STATUS_CHANGE_REQUEST_DETAILS_BY_PK = None
    PAYMENT_DETAILS_BY_PK = None
    SITE_VISIT_DETAILS_BY_PK = None


class SMS:
    OTP_LOGIN_MESSAGE = "Dear {name},24HRS Application login {otp} - COSMOZEAL TECH LLP"
    TEXTLOCAL_HOST = "https://api.textlocal.in/send/?"
