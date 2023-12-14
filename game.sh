#!/bin/env bash

if ! python -c "import argumentation_game" &>/dev/null; then
    if ! python -m pip install .; then
        echo "Failed to install argumentation_game. Are you in the right directory?"
        exit 1
    fi
fi

python -m argumentation_game --game $1 $2
