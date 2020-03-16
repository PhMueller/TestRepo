#!/usr/bin/env sh

if [[ "$USE_SINGULARTIY" == "true" ]]; then
    # Create the coverage report for the singularity example, since it covers more tests.
    pytest -sv --cov=hpolib tests/
    codecov --token=$CODECOV_TOKEN
else
    pytest -sv
fi
