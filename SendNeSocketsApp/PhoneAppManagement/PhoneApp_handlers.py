import asyncio
import logging
import websockets
import json


from SendNeSocketsApp import models
from SendNeSocketsApp.Commons.BlockStates import BlockedStatu

from SendNeSocketsApp.PhoneAppManagement import PhoneApp_utils, PhoneApp_router
from SendNeSocketsApp import handlers

logger = logging.getLogger('handlers-private-phoneApp')



#---------------- Handlers For Temp User ------------------#

@asyncio.coroutine
def userPhone_main_handler(websocket , session_id , isTempPhone = True):
    if isTempPhone:
        phoneApp_Model = PhoneApp_utils.get_TempPhoneDeviceInfo_from_session(session_id)
        if phoneApp_Model is not None:
            # 01 Check Blocked State
            if phoneApp_Model.device_state == models.TempPhoneDevicePrivateUserInfo.DeviceState.Available:
                if phoneApp_Model.blocked_state == BlockedStatu.Running:
                    phoneOwn_objectId = phoneApp_Model.temp_user_private_processor.user_objectId
                    if phoneOwn_objectId is not None:
                        phoneApp_objectId = phoneApp_Model.self_objectId
                        if phoneApp_objectId is not None:
                            phoneApp_clientObjectId = phoneApp_Model.client_objectId
                            if phoneApp_clientObjectId is not None:
                                userConnection = handlers.users_ws_connections.get(phoneOwn_objectId)
                                if userConnection is not None:
                                    userConnection.get("phoneApp_dic")[phoneApp_clientObjectId] = phoneApp_objectId
                                    handlers.phoneApps_ws_connections[phoneApp_objectId] = {
                                        "phoneApp_objectId": phoneApp_objectId,
                                        "phoneApp_clientObjectId": phoneApp_clientObjectId,
                                        "websocket": websocket,
                                        "user_objectId": phoneOwn_objectId
                                    }
                                    ## tell user on be Online

                                    userConnection.get("onlineApp_dic")[phoneApp_clientObjectId] = "connected"
                                    yield from PhoneApp_router.PhoneAppRequestRouter_olineChange(phoneOwn_objectId,
                                                                                        phoneApp_clientObjectId,
                                                                                        "connected")
                                    try:
                                        while websocket.open:
                                            data = yield from websocket.recv()
                                            if not data:
                                                print("\n----- : websocket.recv() : not data : -----------")
                                                continue
                                            logger.debug(data)

                                            print("phoneApp : data == " + str(data))

                                            try:
                                                yield from PhoneApp_router.PhoneAppRequestRouter_request(
                                                    phoneOwn_objectId, phoneApp_clientObjectId, data)
                                            except Exception as e:
                                                logger.error('could not route msg', e)

                                    except websockets.exceptions.InvalidState:  # User disconnected
                                        pass
                                    finally:
                                        del handlers.phoneApps_ws_connections[phoneApp_objectId]
                                        userConnection.get("onlineApp_dic")[phoneApp_clientObjectId] = "disconnected"

                                        yield from PhoneApp_router.PhoneAppRequestRouter_olineChange(
                                            phoneOwn_objectId,
                                            phoneApp_clientObjectId, "disconnected")

                                else:
                                    ## tell user app trying Online : save in databsae
                                    print("\n----------- : phoneApp : User is not connect : ----------------")
                                    #make app disconnect
                                    #raise Exception("phoneApp User is is not connect")
                            else:
                                raise Exception("phoneApp_clientObjectId is null")
                        else:
                            raise Exception("phoneApp_objectId is null")
                    else:
                        raise Exception("phoneOwn_objectId is null")
                else:
                    raise Exception("phoneApp_Model is Blocked")
            else:
                raise Exception("phoneApp_Model is unavailable")
        else:
            raise Exception("phoneApp model is not exist")
    else:
        raise Exception("phoneApp is not support now")


@asyncio.coroutine
def user_requset_transfer_toPhoneApp_handler(stream):
    """
    router a request to user socket
    """
    # TODO: handle no user found exception
    while True:
        """
        router a request to user socket
        """
        # TODO: handle no user found exception
        while True:
            user_objectId, packet = yield from stream.get()

            data = packet.get("data")
            if data is not None:
                if type(data) is dict:
                    phone_objectId = data.get("phone_objectId")
                    if phone_objectId is None:
                        raise Exception("phone_objectId is null from user")
                    else:
                        if type(phone_objectId) is not str:
                            raise Exception("phone_objectId is error type from user")
                        else:
                            user_connection = handlers.users_ws_connections.get(user_objectId)
                            if user_connection is not None:
                                phoneApp_objectId = user_connection.get("phoneApp_dic").get(phone_objectId)
                                if phoneApp_objectId is None:
                                    raise Exception("error in phoneApp_objectId or may is not connect")
                                else:
                                    phoneApp_connection = handlers.phoneApps_ws_connections.get(phoneApp_objectId)
                                    if phoneApp_connection is not None:
                                        data_content = data.get("data_content")
                                        if data_content is not None:
                                            payload = {
                                                "type-content" : "user_transfer",
                                                "data_content" : data_content
                                            }
                                            yield from target_message_phonApp(phoneApp_connection["websocket"],
                                                                              payload)
                                        else:
                                            # here block user
                                            raise Exception("error in data_content : null from user")
                                    else:
                                        raise Exception("error in phoneApp_connection : is not connect")
                            else:
                                raise Exception("may user ws is closed")
                else:
                    raise Exception("error in packet : type")
            else:
                raise Exception("error in packet : null")
            try:
                pass
            except:
                print("--------- : error : ------------")


@asyncio.coroutine
def target_message_phonApp(phonApp_ws, payload):
    """
    Distibuted payload (message) to one connection
    :param conn: connection
    :param payload: payload(json dumpable)
    :return:
    """
    try:
        yield from phonApp_ws.send(json.dumps(payload))
    except Exception as e:
        logger.debug('could not send', e)


#---------------- Handlers For Phone App ------------------#

@asyncio.coroutine
def new_phoneApp_request_handler(stream):
    """
    router a request to user socket
    """
    # TODO: handle no user found exception
    while True:
        user_objectId , phoneApp_clientObjectId , packet = yield from stream.get()

        #data = json.loads(packet)
        data = packet
        if data is not None:
            if user_objectId is not None:
                ## check here later if user is registed or tempUser
                # that by userId length
                user_connection = handlers.users_ws_connections.get(user_objectId)
                if user_connection is not None:
                    payload = {
                        "type-content": "notify",
                        "notify": "sys",
                        "tag": "phoneApp",
                        "type-phoneApp": "transfer",
                        "result": {
                            "device_objectId": phoneApp_clientObjectId,
                            "transfered-data": packet
                        }
                    }
                    yield from handlers.target_message_user(user_connection["websocket"], payload)
                else:
                    # save the result in temp db users result
                    #raise Exception("may user ws is close")
                    # send closing For app
                    pass
            else:
                raise Exception("error in system add user id")
        else:
            raise Exception("error in packet : null")


@asyncio.coroutine
def phoneApp_online_change_handler(stream):
    """
    router a request to user socket
    """
    # TODO: handle no user found exception
    while True:
        user_objectId , phoneApp_clientObjectId , onlineState = yield from stream.get()

        if user_objectId is not None:
            ## check here later if user is registed or tempUser
            # that by userId length
            user_connection = handlers.users_ws_connections.get(user_objectId)
            if user_connection is not None:
                payload = {
                    "type-content": "notify",
                    "notify": "sys",
                    "tag": "device",
                    "type-device": "online-changed",
                    "result": {
                        "statu" : "done" ,
                        "online_state" : onlineState,
                        "device_objectId": phoneApp_clientObjectId,
                    }
                }
                '''
                payload = {
                "type-content": "notify",
                "notify": "sys",
                "tag": "device",
                "type-device": "online-changed",
                "result": {
                    "statu" : "done" ,
                    "devices : {
                    "online_state" : onlineState,
                    "device_objectId": phoneApp_clientObjectId
                    }
                }
                '''
                yield from handlers.target_message_user(user_connection["websocket"], payload)
            else:
                # save the result in temp db users result
                #raise Exception("may user ws is close")
                #notify App to close
                pass
        else:
            raise Exception("error in system add user id")





