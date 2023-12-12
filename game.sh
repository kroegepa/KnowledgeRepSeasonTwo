#!/bin/env bash

set -e

python -m pip install -e .
python -m argumentation_game --game $1 $2
