import asyncio
import json
import logging




#---------------- Handlers For Phone App ------------------#
from SendNeSocketsApp.PhoneAppManagement import PhoneApp_channels


@asyncio.coroutine
def PhoneAppRequestRouter_request(user_objectId , phoneApp_clientObjectId , packet):
    yield from PhoneApp_channels.PhoneApp_request_ForUser.put((user_objectId , phoneApp_clientObjectId , packet))

@asyncio.coroutine
def PhoneAppRequestRouter_olineChange(user_objectId , phoneApp_clientObjectId , onlineState):
    yield from PhoneApp_channels.phoneApp_online_change.put((user_objectId , phoneApp_clientObjectId , onlineState))


