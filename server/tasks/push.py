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
