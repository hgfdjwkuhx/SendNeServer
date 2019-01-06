import asyncio

from SendNeSocketsApp import handlers
from SendNeSocketsApp.management.ClientLocalOper import ClientPhoneDeviceOper


@asyncio.coroutine
def client_phone_device_oper_handler(stream):
    """
    router a request to user socket
    """
    # TODO: handle no user found exception
    while True:
        user_objectId , packet = yield from stream.get()

        data = packet.get("data")
        resultt = None
        if data is not None:
            type_request = data.get("type_way")
            if type_request is not None:
                if type_request == "info_all":
                    resultt = ClientPhoneDeviceOper.infoAll_phone_device(user_objectId, data.get("device_content"))
                else:
                    if type_request == "add_new":
                        resultt = ClientPhoneDeviceOper.new_phone_device(user_objectId , data.get("device_content"))
                    else:
                        raise Exception("error type_request is unknow")


                if resultt is not None:
                    yield from handlers.target_result_user(user_objectId , resultt)
                else:
                    raise Exception("error resultt is null")
            else:
                raise Exception("error type_request is null")

        else:
            raise Exception("error data is null")
