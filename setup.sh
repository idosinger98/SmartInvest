#!/bin/bash -ex
# The -e option would make our script exit with an error if any command
# fails while the -x option makes verbosely it output what it does

# Install Pipenv, the -n option makes sudo fail instead of asking for a
# password if we don't have sufficient privileges to run it
sudo -n dnf install -y pipenv
sudo -n dnf install -y gcc
sudo -n dnf install -y python3-devel mysql-devel

cd /vagrant
# Install dependencies with Pipenv
pipenv sync --dev

# Run database migrations
pipenv run python manage.py migrate

# run our app. setsid, the parentheses and "&" are used to perform a "double
# fork" so that out app stays up after the setup script finishes.
# The app logs are redirected to the `runserver.log` file.
(setsid pipenv run \
	python manage.py runserver 0.0.0.0:8000 > runserver.log 2>&1 &)