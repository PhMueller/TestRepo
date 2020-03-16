#!/usr/bin/env sh

if [[ "$RUN_CODESTYLE" == "true" ]]; then
  pip install pycodestyle flake8
  pwd
  echo "$(pwd) Curr directory"
  pycodestyle --max-line-length=120 ./hpolib
  flake8 --max-line-length=120 ./hpolib
fi
