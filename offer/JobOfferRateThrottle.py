from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class JobOfferRateThrottle(UserRateThrottle, AnonRateThrottle):
    scope = 'user anon'
    THROTTLE_RATES = {
        'user': '5/day',
        'anon': '5/day'
    }