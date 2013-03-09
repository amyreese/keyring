# Copyright 2013 John Reese
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from core import app

from celery import Celery
from gcm import GCM

celery = Celery('gcm', broker=app.config['QUEUE_BROKER'])
gcm = GCM(app.config['GCM_API_KEY'])

@celery.task
def send_message(regid, **kwargs):
    response = gcm.json_request(registration_ids=[regid], **kwargs)

    if 'errors' in response:
        for error, regids in response['errors'].items():
            if error is 'NotRegistered':
                # TODO: remove registration id from database
                pass

    if 'canonical' in response:
        for canonical_id, regid in response['canonical'].items():
            # TODO: update registration id in database
            pass
