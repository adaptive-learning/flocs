test:
	python manage.py test --traceback

check:
	pylint --reports=n --disable=E501,E225,E123,E128 --ignore=migrations,urls.py,wsgi.py flocs

install:
	pip install -r requirements.txt
	python manage.py migrate
