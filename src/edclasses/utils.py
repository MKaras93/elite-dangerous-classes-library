import datetime
from collections import defaultdict
from typing import Tuple, List


def return_first_match(func, items):
    return next(item for item in items if func(item))


class UniqueInstanceMixin:
    registry = {}
    keys = tuple()

    @classmethod
    def create(cls, **kwargs):
        try:
            return cls(**kwargs)
        except InstanceAlreadyExists:
            return cls.get_from_registry(**kwargs)

    @classmethod
    def _get_key(cls, *args, **kwargs):
        if args:
            instance = args[0]
            return tuple(getattr(instance, attr) for attr in cls.keys)
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
            raise InstanceAlreadyExists
        self.__class__.registry[obj_key] = self
        super().__init__()

    def remove_from_registry(self):
        obj_key = self._get_key(**self.__dict__)
        self.registry.pop(obj_key)

    def delete(self):
        self.remove_from_registry()


class OneToOneRelation(UniqueInstanceMixin):
    registry = {}
    keys = (
        "parent_class_name",
        "child_class_name",
    )

    def __init__(self, parent_class_name: str, child_class_name: str):
        self.parent_class_name = parent_class_name
        self.child_class_name = child_class_name
        self.parent_side = {}
        self.child_side = {}
        super().__init__()

    def set_for_parent(self, parent_obj, child_obj):
        old_child = self.get_for_parent(parent_obj)

        if old_child and child_obj is not old_child:
            self._delete_link(parent_obj, old_child)

        if child_obj is not None:
            self._add_link(parent_obj, child_obj)

    def get_for_parent(self, parent_obj):
        return self.parent_side.get(parent_obj, None)

    def set_for_child(self, child_obj, parent_obj):
        old_parent = self.get_for_child(child_obj)

        if old_parent and parent_obj is not old_parent:
            self._delete_link(old_parent, child_obj)

        if parent_obj is not None:
            self._add_link(parent_obj, child_obj)

    def get_for_child(self, child_obj):
        return self.child_side.get(child_obj, None)

    def _delete_link(self, parent_obj, child_obj):
        self.parent_side.pop(parent_obj)
        self.child_side.pop(child_obj)

    def _add_link(self, parent_obj, child_obj):
        self.parent_side[parent_obj] = child_obj
        self.child_side[child_obj] = parent_obj


class OneToManyRelation(OneToOneRelation):
    registry = {}

    def __init__(self, parent_class_name: str, child_class_name: str):
        super().__init__(parent_class_name, child_class_name)
        self.parent_side = defaultdict(list)

    def _add_link(self, parent_obj, child_obj):
        self.parent_side[parent_obj].append(child_obj)
        self.child_side[child_obj] = parent_obj

    def _delete_link(self, parent_obj, child_obj):
        self.parent_side[parent_obj].remove(child_obj)
        self.child_side.pop(child_obj)

    def get_for_parent(self, parent_obj):
        return self.parent_side.get(parent_obj, list())

    def set_for_parent(self, parent_obj, children: List):
        old_children = self.get_for_parent(parent_obj)
        for child in old_children:
            self.child_side.pop(child)

        for child in children:
            old_parent = self.get_for_child(child)
            if old_parent is not None:
                self._delete_link(old_parent, child)
            self.child_side[child] = parent_obj

        self.parent_side[parent_obj] = children

    def set_for_child(self, child_obj, parent_obj):
        old_parent = self.get_for_child(child_obj)

        if parent_obj is old_parent:
            return

        if old_parent is not None:
            self._delete_link(old_parent, child_obj)

        if parent_obj is not None:
            self._add_link(parent_obj, child_obj)


class InstanceAlreadyExists(Exception):
    pass


class AutoRefreshMixin:
    refreshed_fields = tuple()
    adapter = None
    EXPIRATION_TIME_MINUTES = 15

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._set_adapter(**kwargs)

    def _set_adapter(self, **kwargs):
        self.adapter = kwargs.get("adapter", self.adapter)

    def _get_new_expiration_registry(self):
        get_atr = super().__getattribute__
        expiration_registry = {item: None for item in get_atr("refreshed_fields")}
        self._expiration_registry = expiration_registry
        return expiration_registry

    def __getattribute__(self, item):
        get_atr = super().__getattribute__
        try:
            expiration_registry = get_atr("_expiration_registry")
        except AttributeError:
            expiration_registry = get_atr("_get_new_expiration_registry")()

        try:
            expiration_date = expiration_registry[item]
        except KeyError:
            return get_atr(item)

        is_expired = (
            expiration_date is None or expiration_date <= datetime.datetime.utcnow()
        )

        if is_expired:
            adapter = get_atr("adapter")
            refresh_func = getattr(adapter, item)
            value = refresh_func(
                self
            )  # TO CHECK: this will call getattribute again, can lead to loops

            expiration_registry[item] = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=get_atr("EXPIRATION_TIME_MINUTES")
            )
            setattr(self, item, value)

        return get_atr(item)
