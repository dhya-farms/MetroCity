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
    USER_LIST = "user_list:{name}:{mobile_no}:{role}:{page}"
    CUSTOMER_LIST = "customer_list:{name}:{email}:{mobile_no}:{page}"
    PROPERTY_LIST = "property_list:{property_type}:{area_of_purpose}:{phase_number}"
    PHASE_LIST = "phase_list:{property_id}:{phase_number}:{status}"
    PLOT_LIST = "plot_list:{phase_id}:{is_corner_site}:{availability}:{facing}:{soil_type}"
    CRM_LEAD_LIST = "crm_lead_list:{plot_id}:{customer_id}:{assigned_so_id}:{current_status}"
    STATUS_CHANGE_REQUEST_LIST = "status_change_list:{crm_lead_id}:{requested_by_id}:{approved_by_id}:{requested_status}:{approval_status}"
    PAYMENT_LIST = "payment_list:{crm_lead_id}:{payment_mode}:{payment_status}:{payment_for}:{start_time}:{end_time}"
    SITE_VISIT_LIST = "site_visit_list:{crm_lead_id}:{is_pickup}:{pickup_date}:{is_drop}"

    # DETAILS
    USER_DETAILS_BY_PK = "user_details_by_pk:{pk}"
    CUSTOMER_DETAILS_BY_PK = "customer_details_by_pk:{pk}"
    PROPERTY_DETAILS_BY_PK = "property_details_by_pk:{pk}"
    PHASE_DETAILS_BY_PK = "phase_details_by_pk:{pk}"
    PLOT_DETAILS_BY_PK = "plot_details_by_pk:{pk}"
    CRM_LEAD_DETAILS_BY_PK = "crm_lead_details_by_pk:{pk}"
    STATUS_CHANGE_REQUEST_DETAILS_BY_PK = "status_change_request_details_by_pk:{pk}"
    PAYMENT_DETAILS_BY_PK = "payment_details_by_pk:{pk}"
    SITE_VISIT_DETAILS_BY_PK = "site_visit_details_by_pk:{pk}"


class SMS:
    OTP_LOGIN_MESSAGE = "Dear {name},24HRS Application login {otp} - COSMOZEAL TECH LLP"
    TEXTLOCAL_HOST = "https://api.textlocal.in/send/?"
