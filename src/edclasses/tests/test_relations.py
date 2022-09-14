from ..utils import OneToManyRelation


class Parent:
    _children_relation = OneToManyRelation.create(
        parent_class_name="Parent", child_class_name="Child"
    )

    def __init__(self, children=None):
        self.children = children or []

    def _children_setter(self, value):
        self._children_relation.set_for_parent(self, value)

    def _children_getter(self):
        return self._children_relation.get_for_parent(self)

    children = property(fget=_children_getter, fset=_children_setter)


class Child:
    _parent_relation = OneToManyRelation.create(
        parent_class_name="Parent", child_class_name="Child"
    )

    def __init__(self, parent=None):
        self.parent = parent

    def _parent_setter(self, value):
        self._parent_relation.set_for_child(self, value)

    def _parent_getter(self):
        return self._parent_relation.get_for_child(self)

    parent = property(fget=_parent_getter, fset=_parent_setter)


class TestOneToManyRelation:
    class TestChildSide:
        def test_removing_parent_removes_link(self):
            parent = Parent()
            child = Child(parent=parent)
            assert child.parent == parent
            assert parent.children == [child]

            child.parent = None

            assert child.parent is None
            assert parent.children == []

        def test_adding_parent_creates_link(self):
            parent = Parent()
            child = Child()

            child.parent = parent

            assert child.parent is parent
            assert parent.children == [child]

        def test_replacing_parent_replaces_link(self):
            old_parent = Parent()
            new_parent = Parent()
            child = Child(parent=old_parent)
            assert old_parent is not new_parent
            assert child.parent is old_parent
            assert old_parent.children == [child]

            child.parent = new_parent

            assert child.parent is new_parent
            assert new_parent.children == [child]
            assert old_parent.children == []

    class TestParentSide:
        def test_removing_children_removes_links(self):
            child1 = Child()
            child2 = Child()
            parent = Parent(children=[child1, child2])
            assert child1.parent is parent
            assert child2.parent is parent

            parent.children = []

            assert child1.parent is None
            assert child2.parent is None

        def test_adding_children_adds_links(self):
            child1 = Child()
            child2 = Child()
            parent = Parent(children=[])

            parent.children = [child1, child2]

            assert child1.parent is parent
            assert child2.parent is parent

        def test_stealing_children_replaces_links(self):
            old_parent = Parent()
            child1 = Child(parent=old_parent)
            child2 = Child(parent=old_parent)
            new_parent = Parent()
            assert old_parent.children == [child1, child2]
            new_parent.children = [child2]

            assert child1.parent is old_parent
            assert child2.parent is new_parent
            assert new_parent.children == [child2]
            assert old_parent.children == [child1]
