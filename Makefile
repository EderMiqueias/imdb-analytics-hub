.PHONY: up_db up_mysql_db venv install

up_db:
	$(MAKE) up_mysql_db

up_mysql_db:
	docker-compose up mysql_db

venv:
	python3 -m venv venv
	pip install --upgrade pip

install:
	pip install -r requirements.txt
