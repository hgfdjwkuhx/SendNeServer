import asyncio
import json
import logging

from SendNeSocketsApp.PhoneAppManagement import PhoneApp_channels
from SendNeSocketsApp import channels

logger = logging.getLogger('django-SenderNe-TempClientWS')


class TempUserRequestRouter(object):
    MESSAGE_QUEUES = {
        'campaign' : channels.client_processor_requests,
        'device': channels.client_phoneDevice_oper,
        'phonapp' : PhoneApp_channels.user_tarnsfer_request_ForPhoneApp
    }

    def __init__(self, data , user_objectId):
        try:
            self.user_objectId = user_objectId
            self.packet = json.loads(data)
        except Exception as e:
            logger.debug('could not load json: {}'.format(str(e)))

    def get_packet_type(self):
        return self.packet['data'].get('tag')

    @asyncio.coroutine
    def __call__(self):
        logger.debug('routing message: {}'.format(self.packet))
        send_queue = self.get_send_queue()
        yield from send_queue.put((self.user_objectId , self.packet))

    def get_send_queue(self):
        return self.MESSAGE_QUEUES[self.get_packet_type()]
