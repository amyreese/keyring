Keyring
=======

Client
------

Requires:

* Android SDK versions 2.3 (API 10), 4.0 (API 14), and 4.2.2 (API 17)
* Google APIS, plus all Google extras
* Apache Ant


Server
------

Requires:

* Python 2.7
* RabbitMQ (or other queue broker supported by Celery)
* MySQL (or other database supported by SQLAlchemy)
	
Install the necessary python modules, ideally within a virtualenv:

	pip install celery flask py-bcrypt pymysql python-gcm python-memcached sqlalchemy

Optional modules, for development/debugging features:

	pip install ipython


License
-------

Copyright 2013 John Reese

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
