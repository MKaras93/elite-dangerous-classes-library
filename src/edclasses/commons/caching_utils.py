import datetime

_NEVER_EXPIRE = 0


class ExpiringCachedPropertyMixin:
    def _clear_property(self, item):
        get_attr = super().__getattribute__
        registry = get_attr("expiring_properties_registry")
        if item not in registry:
            raise ValueError(f"{item} is not a registered property!")  # TODO correct

        cache = get_attr("__dict__")
        cache.pop(item, None)
        expire_key = self._get_expiration_key(item)
        cache.pop(expire_key, None)

    @staticmethod
    def _get_expiration_key(item):
        return f"{item}_expiration_time"

    def _get_new_expiration_time(self, lifetime_in_seconds):
        if lifetime_in_seconds:
            return datetime.datetime.utcnow() + datetime.timedelta(
                seconds=lifetime_in_seconds
            )
        else:
            return None

    @staticmethod
    def _is_expired(expiration_time):
        if expiration_time and datetime.datetime.utcnow() >= expiration_time:
            return True
        return False

    def __getattribute__(self, item):
        get_attr = super().__getattribute__
        registry = get_attr("expiring_properties_registry")
        try:
            item_lifetime = registry[item]
        except KeyError:
            return get_attr(item)

        cache = get_attr("__dict__")
        expiration_key = get_attr("_get_expiration_key")(item)
        expiration_time = cache.get(expiration_key)
        time_expired = expiration_time and datetime.datetime.utcnow() >= expiration_time
        if time_expired:
            cache.pop(item, None)

        val = super().__getattribute__(item)

        if expiration_time is None or time_expired:
            cache[expiration_key] = get_attr("_get_new_expiration_time")(
                lifetime_in_seconds=item_lifetime
            )
        return val

    def __setattr__(self, key, value):
        get_attr = super().__getattribute__
        registry = get_attr("expiring_properties_registry")
        __dict__ = get_attr("__dict__")
        if key in registry:
            expiration_key = get_attr("_get_expiration_key")(key)
            __dict__[expiration_key] = _NEVER_EXPIRE

        return super().__setattr__(key, value)
