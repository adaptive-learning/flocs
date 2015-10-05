update:
	@echo "== Install Python dependencies. =="
	pip install -r requirements.txt --quiet
	@echo "== Set up database. =="
	python manage.py migrate
	# TODO: load fixtures
	@echo "== Install frontend dependencies. =="
	cd frontend && \
	  npm update && \
	  bower update && \
	  grunt development-build

test:
	python manage.py test --traceback

check:
	pylint --reports=n --disable=E501,E225,E123,E128 --ignore=migrations,urls.py,wsgi.py flocs
