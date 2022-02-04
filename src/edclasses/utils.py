def return_first_match(func, items):
    return next(item for item in items if func(item))


class UniqueInstanceMixin:
    registry = {}
    keys = tuple()

    @classmethod
    def create(cls, **kwargs):
        try:
            return cls(**kwargs)
        except ValueError:
            return cls.get_from_registry(**kwargs)

    @classmethod
    def _get_key(cls, *args, **kwargs):
        if args:
            instance = args[0]
            return tuple(getattr(instance,attr) for attr in cls.keys)
        else:
            return tuple(kwargs[attr] for attr in cls.keys)

    @classmethod
    def get_from_registry(cls, **kwargs):
        obj_key = cls._get_key(**kwargs)
        return cls.registry.get(obj_key)

    def __init__(self, *args, **kwargs):
        obj_key = self._get_key(self)
        obj = self.__class__.registry.get(obj_key)
        if obj is not None:
            raise ValueError
        self.__class__.registry[obj_key] = self
        super().__init__()

    def remove_from_registry(self):
        obj_key = self._get_key(**self.__dict__)
        self.registry.pop(obj_key)

    def delete(self):
        self.remove_from_registry()
