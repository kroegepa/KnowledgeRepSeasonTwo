# KnowledgeRepSeasonTwo

To run the tests on the admissability labeler, first install pytest, then do:
```sh
# Install the package locally to be able to test it
python -m pip install -e .

python -m pytest tests/
```

Part two of these tests perform the exact same tests as those for part 2 from `NonmonotonicDefaultlogicLec1-1.pdf` in the assignment for our chosen semantics, and test if the given nodes being in and out are in an admissable labeling.
