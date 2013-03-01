keyring
=======


Server
------

Requires:

	Python 2.7
	RabbitMQ (or other queue broker supported by Celery)
	MySQL (or other database supported by SQLAlchemy)
	
Install the necessary python modules, ideally within a virtualenv:

	pip install celery flask py-bcrypt pymysql python-gcm python-memcached sqlalchemy

Optional modules, for development/debugging features:

	pip install ipython
