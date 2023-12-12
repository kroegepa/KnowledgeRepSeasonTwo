from argumentation_game.labeling import Label
from argumentation_game.argument_graph import ArgumentGraph
from argumentation_game.recursive_shenanigans import is_in_admissable_labeling

from .helpers import DATA_PATH, load_json


class TestAssignmentTwoOne:
    data = ArgumentGraph.from_json(load_json(DATA_PATH / "example1.json"))

    def test_one_one(self):
        assert is_in_admissable_labeling(self.data, 0, Label.In) is True
        assert is_in_admissable_labeling(self.data, 0, Label.Out) is False

    def test_one_two(self):
        assert is_in_admissable_labeling(self.data, 5, Label.In) is False
        assert is_in_admissable_labeling(self.data, 5, Label.Out) is True


class TestAssignmentTwoTwo:
    data = ArgumentGraph.from_json(load_json(DATA_PATH / "example2.json"))

    def test_two_one(self):
        assert is_in_admissable_labeling(self.data, 2, Label.In) is True
        assert is_in_admissable_labeling(self.data, 2, Label.Out) is True

    def test_two_two(self):
        assert is_in_admissable_labeling(self.data, 3, Label.In) is True
        assert is_in_admissable_labeling(self.data, 3, Label.Out) is True

    def test_two_three(self):
        assert is_in_admissable_labeling(self.data, 0, Label.In) is True
        assert is_in_admissable_labeling(self.data, 0, Label.Out) is False


class TestAssignmentTwoThree:
    data = ArgumentGraph.from_json(load_json(DATA_PATH / "example3.json"))

    def test_two_one(self):
        assert is_in_admissable_labeling(self.data, 1, Label.In) is True
        assert is_in_admissable_labeling(self.data, 1, Label.Out) is True

    def test_two_two(self):
        assert is_in_admissable_labeling(self.data, 3, Label.In) is True
        assert is_in_admissable_labeling(self.data, 3, Label.Out) is False

    def test_two_three(self):
        assert is_in_admissable_labeling(self.data, 4, Label.In) is False
        assert is_in_admissable_labeling(self.data, 4, Label.Out) is True
