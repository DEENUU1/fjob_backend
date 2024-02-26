from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class JobOfferRateUserThrottle(UserRateThrottle, AnonRateThrottle):
    """
    Custom throttle class for limiting the rate of JobOffer rating by user.

    Attributes:
    - scope: The scope of the throttle, set to 'user'.
    - THROTTLE_RATES: Throttle rates configuration, limiting to 5 requests per day for users.
    """
    scope = 'user'
    THROTTLE_RATES = {
        'user': '5/day'
    }


class JobOfferRateAnonThrottle(UserRateThrottle, AnonRateThrottle):
    """
    Custom throttle class for limiting the rate of JobOffer rating by anonymous users.

    Attributes:
    - scope: The scope of the throttle, set to 'anon'.
    - THROTTLE_RATES: Throttle rates configuration, limiting to 5 requests per day for anonymous users.
    """
    scope = 'anon'
    THROTTLE_RATES = {
        'anon': '5/day'
    }
