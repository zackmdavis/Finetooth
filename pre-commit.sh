#!/bin/bash

# Move/rename this to .git/hooks/pre-commit to run the Django tests
# before commiting.

./manage.py test core
