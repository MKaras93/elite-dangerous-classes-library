import datetime
from typing import Optional, Any

_NEVER_EXPIRE = 0  # TODO: this could be obj()


class ExpiringCachedPropertyMixin:
    """
    To be used with @cached_property_decorator.

    Add this mixin to the class, if you want its cached property to expire after a set time.

    To mark a method as expiring property:

    1. Add @functools.cached_property decorator on the method which you want to cache for a limited period of time.
    2. Add attribuge 'expiring_properties_registry={}' to your class.
    3. Register your method in the expiring_properties_registry as {'<method_name>': <lifetime_in_seconds>}.

    When you first call obj.<name_of_cached_property>, it will be calculated and saved with an expiration date.
    When you call obj.<name_of_cached_property> and the time has expired, it will be recalculated.
    When you set your property manually, or pass it during class initialization, it will never expire.
    If you set None as lifetime_in_seconds, it will never expire.
    You can use self.clear_property(property_name) to manually clear the cache on given attribute
    """
    def _clear_property(self, item: str) -> None:
        get_attr = super().__getattribute__
        try:
            registry = get_attr("expiring_properties_registry")
        except AttributeError:
            raise NotImplemented(f"You must define expiring_properties_registry on {self.__class__.__name__} to use"
                                 " ExpiringCachedPropertyMixIn")
        if item not in registry:
            raise ValueError(f"{self.__class__.__name__}.{item} is registered!")

        cache = get_attr("__dict__")
        cache.pop(item, None)
        expire_key = self._get_expiration_key(item)
        cache.pop(expire_key, None)

    @staticmethod
    def _get_expiration_key(item: str) -> str:
        return f"{item}_expiration_time"

    def _get_new_expiration_time(self, lifetime_in_seconds: int) -> Optional[datetime.datetime]:
        if lifetime_in_seconds:
            return datetime.datetime.utcnow() + datetime.timedelta(
                seconds=lifetime_in_seconds # TODO: change to minutes
            )
        else:
            return None

    @staticmethod
    def _is_expired(expiration_time: [datetime.datetime, int]) -> bool:
        if expiration_time and datetime.datetime.utcnow() >= expiration_time:
            return True
        return False

    def __getattribute__(self, item: str) -> Any:
        get_attr = super().__getattribute__
        try:
            registry = get_attr("expiring_properties_registry")
        except AttributeError:
            raise NotImplemented(f"You must define expiring_properties_registry on {self.__class__.__name__} to use"
                                 " ExpiringCachedPropertyMixIn")

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

        val = get_attr(item)

        if expiration_time is None or time_expired:
            cache[expiration_key] = get_attr("_get_new_expiration_time")(
                lifetime_in_seconds=item_lifetime
            )
        return val

    def __setattr__(self, key: str, value: Any) -> None:
        get_attr = super().__getattribute__

        try:
            registry = get_attr("expiring_properties_registry")
        except AttributeError:
            raise NotImplemented(f"You must define expiring_properties_registry on {self.__class__.__name__} to use"
                                 " ExpiringCachedPropertyMixIn")

        __dict__ = get_attr("__dict__")
        if key in registry:
            expiration_key = get_attr("_get_expiration_key")(key)
            __dict__[expiration_key] = _NEVER_EXPIRE

        return super().__setattr__(key, value)
