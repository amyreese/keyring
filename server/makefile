
debug:
	python2 app.wsgi

server:
	uwsgi --http 0.0.0.0:8000 --file app.wsgi --touch-reload app.wsgi

schema:
	python2 app.wsgi schema

shell:
	python2 -i app.wsgi shell

.PHONY:
submodules:
	git submodule init && git submodule sync && git submodule update

.PHONY:
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

