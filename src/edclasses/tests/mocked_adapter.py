class MockedAdapter:
    """
    Dummy Adapter which returns the value which is already on the object.
    """

    @staticmethod
    def _get_getter_name(attr):
        return f"_{attr}_getter"

    def __getattr__(self, attr):
        getter_name = self._get_getter_name(attr)

        def _return_value_from_obj(*args):
            obj = next(iter(args))
            return getattr(obj, getter_name)()

        return _return_value_from_obj
