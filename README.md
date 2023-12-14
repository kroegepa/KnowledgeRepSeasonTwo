# KnowledgeRepSeasonTwo

Code submission for the second assignment of the VU course Knowledge Representation

To run any code, first, install the code as a package. Do this with:
```sh
python -m pip install .
```

After this, the game can be run as follows:
```sh
python -m argumentation_game [--game/-g] input.json argument
```

After this, the credulous decision on the admissibility semantics can be run as follows:
```sh
python -m argumentation_game input.json argument
```
Under the hood, this will perform the argumentation game with all possible steps in a tree search, and then see if there is a way to win the game with this as a starting argument. We didn't do it this way because it's the most efficient algorithm there is (the one from the slides is probably way better,) but because it seemed fun and in spirit with the first part.

To run both as separate executables, in case that is needed for grading, you can run:
```sh
# Play the game
./game.sh input.json argument

# Perform the decision process
./admissable_decision.sh input.json argument
```
This will also run the pip install, in case that wasn't done already.

---

To run the tests on the admissibility labeler, first install pytest, then do:
```sh
# Install the package locally to be able to test it
python -m pip install -e .

python -m pytest tests/
```

Part two of these tests perform the same tests as those for part 2 from `NonmonotonicDefaultlogicLec1-1.pdf` in the assignment for our chosen semantics and test if the given nodes being in and out are in an admissible labeling.

To get the performance of these, run with `--durations`:
```
python -m pytest --durations=0 tests/test_part_two.py
```
