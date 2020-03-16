#!/usr/bin/env sh

if [[ "$USE_SINGULARTIY" == "true" ]]; then
    # Create the coverage report for the singularity example, since it covers more tests.
    pytest --cov=hpolib
    codecov --token=$CODECOV_TOKEN
else
    pytest
fi
