from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class JobOfferRateUserThrottle(UserRateThrottle, AnonRateThrottle):
    scope = 'user'
    THROTTLE_RATES = {
        'user': '5/day'
    }


class JobOfferRateAnonThrottle(UserRateThrottle, AnonRateThrottle):
    scope = 'anon'
    THROTTLE_RATES = {
        'anon': '5/day'
    }
