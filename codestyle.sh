if [[ "$RUN_CODESTYLE" == "true" ]]; then
  pip install .[codestyle]
  pycodestyle --max-line-length=120 ./hpolib
  flake8 --max-line-length=120 ./hpolib
fi
