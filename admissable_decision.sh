#!/bin/env bash

set -e

python -m pip install -e .
python -m argumentation_game --no-game $1 $2
