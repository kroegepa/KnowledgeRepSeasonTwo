import pytest
from argumentation_game import Label, ArgumentGraph, try_admissability

from .helpers import DATA_PATH, load_json


class TestExamples:
    exampes = {
        "0": ArgumentGraph.from_json(load_json(DATA_PATH / "example0.json")),
        "1": ArgumentGraph.from_json(load_json(DATA_PATH / "example1.json")),
        "2": ArgumentGraph.from_json(load_json(DATA_PATH / "example2.json")),
        "3": ArgumentGraph.from_json(load_json(DATA_PATH / "example3.json")),
    }

    @pytest.mark.parametrize(
        "data,node,label",
        [
            # 0
            ("0", 2, Label.In),
            ("0", 6, Label.In),
            ("0", 4, Label.In),
            ("0", 1, Label.In),
            ("0", 5, Label.Out),
            ("0", 3, Label.Out),
            ("0", 0, Label.Out),
            # 1
            ("1", 5, Label.Out),
            ("1", 4, Label.In),
            ("1", 2, Label.In),
            ("1", 3, Label.Out),
            ("1", 2, Label.In),
            ("1", 1, Label.Out),
            # 2
            ("2", 4, Label.Out),
            ("2", 3, Label.In),
            ("2", 2, Label.Out),
            ("2", 2, Label.In),
            ("2", 0, Label.In),
            ("2", 1, Label.Out),
            ("2", 3, Label.Out),
            # 3
            ("3", 0, Label.Out),
            ("3", 1, Label.In),
            ("3", 2, Label.Out),
            ("3", 3, Label.In),
            ("3", 4, Label.Out),
            ("3", 0, Label.In),
            ("3", 1, Label.Out),
        ],
    )
    def test_admissable(self, data, node, label):
        ret = try_admissability(self.exampes[data], node, label)
        assert ret is not None
        assert self.exampes[data].is_admissable(ret)
        assert ret[node] == label
        assert all(isinstance(l, Label) for l in ret)

    @pytest.mark.parametrize(
        "data, node,label",
        [
            # 0
            ("0", 2, Label.Out),
            ("0", 6, Label.Out),
            ("0", 4, Label.Out),
            ("0", 1, Label.Out),
            ("0", 5, Label.In),
            ("0", 3, Label.In),
            ("0", 0, Label.In),
            # 1
            ("1", 5, Label.In),
            ("1", 4, Label.Out),
            ("1", 2, Label.Out),
            ("1", 3, Label.In),
            ("1", 2, Label.Out),
            ("1", 1, Label.In),
            # 2
            ("2", 4, Label.In),
            ("2", 0, Label.Out),
            ("2", 1, Label.In),
            # 3
            ("3", 2, Label.In),
            ("3", 3, Label.Out),
            ("3", 4, Label.In),
        ],
    )
    def test_inadmissable(self, data, node, label):
        assert try_admissability(self.exampes[data], node, label) is None
