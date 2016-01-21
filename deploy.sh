#!/bin/sh
# deployment script run by Viper server after push

echo "Starting deploy script"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

#requirements
pip install -r $DIR/requirements.txt
cd frontend && \
  npm install && \
  bower install && \
  grunt production-build

cd $DIR

# database
python $DIR/manage.py migrate --noinput
python $DIR/manage.py loaddata tasks/fixtures/tasks.xml
python $DIR/manage.py loaddata practice/fixtures/instructions.json
python $DIR/manage.py generate_tasks_difficulty

# static files
python $DIR/manage.py collectstatic --noinput

# logs
touch $LOGGING_DIR/practice.log
touch $LOGGING_DIR/requests.log
