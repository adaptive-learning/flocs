.PHONY: update \
		dependencies backend-dependencies frontend-dependencies \
		test test-backend test-frontend \
		check check-backend check-frontend \
		db-setup db-migrate db-load-data admin \
		export-data-to-csv logs

# -----------------------------------------------------------

update: dependencies logs db-setup

# -----------------------------------------------------------

dependencies: backend-dependencies frontend-dependencies

backend-dependencies:
	@echo "== Install Python dependencies. =="
	pip install -r requirements.txt

frontend-dependencies:
	@echo "== Install frontend dependencies. =="
	cd frontend && \
	  npm update && \
	  bower update && \
	  grunt development-build

# -----------------------------------------------------------

test: test-backend test-frontend

test-backend:
	@echo "===== Backend tests ====="
	python manage.py test --traceback

test-frontend:
	@echo "===== Frontend tests ====="
	cd frontend && \
	  grunt karma

# -----------------------------------------------------------

check: check-backend check-frontend

check-backend:
	@echo "===== Backend linting ====="
	pylint --reports=n --disable=E501,E225,E123,E128 --ignore=migrations,urls.py,wsgi.py practice

check-frontend:
	@echo "===== Frontend linting ====="
	cd frontend && \
	  grunt lint


# -----------------------------------------------------------

db-setup: db-flush db-migrate admin db-load-data

db-migrate:
	@echo "===== Set up database ====="
	python manage.py migrate --noinput

db-flush:
	python manage.py flush --noinput

db-load-data:
	python manage.py loaddata blocks/fixtures/blocks.xml
	python manage.py loaddata blocks/fixtures/toolboxes.xml
	python manage.py loaddata concepts/fixtures/concepts.xml
	python manage.py loaddata tasks/fixtures/tasks.xml
	python manage.py loaddata concepts/fixtures/instructions.json

admin:
	python manage.py create_admin

# -----------------------------------------------------------

logs:
	@mkdir -p logs >/dev/null
	touch logs/practice.log
	touch logs/requests.log

# -----------------------------------------------------------

export-data-to-csv:
	python manage.py export_data_to_csv
