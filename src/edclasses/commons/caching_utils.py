import datetime
from functools import cached_property
_NOT_FOUND = object()


class cached_property_ttl(cached_property):
    def _get_expiration_key(self):
        return f"{self.attrname}_expiration_time"

    def _get_new_expiration_time(self):
        return datetime.datetime.utcnow() + datetime.timedelta(seconds=5)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.attrname is None:
            raise TypeError(
                "Cannot use cached_property instance without calling __set_name__ on it.")
        try:
            cache = instance.__dict__
        except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
            msg = (
                f"No '__dict__' attribute on {type(instance).__name__!r} "
                f"instance to cache {self.attrname!r} property."
            )
            raise TypeError(msg) from None
        expiration_key = self._get_expiration_key()
        expiration_time = cache.get(expiration_key)
        if expiration_time and datetime.datetime.utcnow() >= expiration_time:
            cache.pop(self.attrname)
            val = _NOT_FOUND
        else:
            val = cache.get(self.attrname, _NOT_FOUND)
        if val is _NOT_FOUND:
            with self.lock:
                # check if another thread filled cache while we awaited lock
                val = cache.get(self.attrname, _NOT_FOUND)
                if val is _NOT_FOUND:
                    val = self.func(instance)
                    try:
                        cache[self.attrname] = val
                        cache[expiration_key] = self._get_new_expiration_time()
                    except TypeError:
                        msg = (
                            f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                            f"does not support item assignment for caching {self.attrname!r} property."
                        )
                        raise TypeError(msg) from None
        return val
