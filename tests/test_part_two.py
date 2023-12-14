from argumentation_game import Label, ArgumentGraph, is_in_admissable_labeling

from .helpers import DATA_PATH, load_json

NR_ITERATIONS = 10**5


class TestAssignmentTwoOne:
    data = ArgumentGraph.from_json(load_json(DATA_PATH / "example1.json"))

    def test_one_one(self):
        for _ in range(NR_ITERATIONS):
            assert is_in_admissable_labeling(self.data, 0) is True

    def test_one_two(self):
        for _ in range(NR_ITERATIONS):
            assert is_in_admissable_labeling(self.data, 5) is False


class TestAssignmentTwoTwo:
    data = ArgumentGraph.from_json(load_json(DATA_PATH / "example2.json"))

    def test_two_one(self):
        for _ in range(NR_ITERATIONS):
            assert is_in_admissable_labeling(self.data, 2) is True

    def test_two_two(self):
        for _ in range(NR_ITERATIONS):
            assert is_in_admissable_labeling(self.data, 3) is True

    def test_two_three(self):
        for _ in range(NR_ITERATIONS):
            assert is_in_admissable_labeling(self.data, 0) is True


class TestAssignmentTwoThree:
    data = ArgumentGraph.from_json(load_json(DATA_PATH / "example3.json"))

    def test_three_one(self):
        for _ in range(NR_ITERATIONS):
            assert is_in_admissable_labeling(self.data, 1) is True

    def test_three_two(self):
        for _ in range(NR_ITERATIONS):
            assert is_in_admissable_labeling(self.data, 3) is True

    def test_three_three(self):
        for _ in range(NR_ITERATIONS):
            assert is_in_admissable_labeling(self.data, 4) is False
