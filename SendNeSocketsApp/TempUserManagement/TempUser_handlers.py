import asyncio
import logging
import websockets
import json

from SendNeSocketsApp.Commons.BlockStates import BlockedStatu
from SendNeSocketsApp.TempUserManagement import TempUser_router
from SendNeSocketsApp.TempUserManagement import TempUser_utils
from SendNeSocketsApp import handlers



logger = logging.getLogger('handlers-private-tempUser')


tempUsers_ws_connections = {}

#---------------- Handlers For Temp User ------------------#

@asyncio.coroutine
def main_temp_user_handler(websocket , session_id):
    tempUser_model = TempUser_utils.get_tempUserProcessorInfo_from_session(session_id)
    if tempUser_model is not None:
        tempUser_objectId = tempUser_model.user_objectId
        # 01 check user_objectId
        #
        #
        #

        # 02 Check Blocked State
        blocked_statu = tempUser_model.blocked_state
        # Check Blocked State new
        if blocked_statu == BlockedStatu.JustAdd:
            TempUser_utils.set_Processor_For_tempUserInfo(tempUser_model)
            blocked_statu = tempUser_model.blocked_state
            #check if processor null
            if tempUser_model.processor_info is None:
                raise Exception("Temp user processor_info is null")
            else:

                pass
                #tell Processor add Temp User

        # 04 check blocked_statu
        if not blocked_statu == BlockedStatu.Running:
            # save in temp db
            raise Exception("Temp user is Blocked")
        else:

            # 05 Check processor
            if tempUser_model.processor_info is None:
                raise Exception("user have not processor info")

            else:
                # 06 Check processor ws
                processor_ws = handlers.processors_ws_connections.get(
                    tempUser_model.processor_info.processor_ObjectId)
                if processor_ws is not None:
                    # 07 check exsist
                    # if tempUsers_ws_connections.get(tempUser_objectId) is not None:
                    #   del tempUsers_ws_connections[tempUser_objectId]

                    handlers.users_ws_connections[tempUser_objectId] = {
                        "processor_objectId": processor_ws["processor_objectId"],
                        "websocket": websocket,
                        "user_objectId": tempUser_objectId,
                        "phoneApp_dic": TempUser_utils.get_tempPhoneAppDic_from_tempUser_model(tempUser_model),
                        "onlineApp_dic": {}
                    }

                    # tempUsers_ws_connections[tempUser_objectId] = {
                    # "websocket": websocket,
                    # "tempUser_objectId": tempUser_objectId,
                    # "processor_ws" : processor_ws
                    # }

                    try:
                        while websocket.open:
                            data = yield from websocket.recv()
                            if not data:
                                print("\n----- : tempUser_websocket.recv() : not data : -----------")
                                continue
                            logger.debug(data)
                            print("temp_client : data == " + str(data))
                            # as temp truing
                            # main_tag_handler(data)

                            try:
                                # yield from router.MessageRouter(data)()
                                # as temp for temp user
                                # temp user uses original user router
                                yield from TempUser_router.TempUserRequestRouter(data, tempUser_objectId)()
                                pass
                            except Exception as e:
                                logger.error('could not route msg', e)

                    except websockets.exceptions.InvalidState:  # User disconnected
                        pass
                    finally:
                        #del tempUsers_ws_connections[tempUser_objectId]
                        del handlers.users_ws_connections[tempUser_objectId]
                        print("\n----------------- Temp User Closing -------------------------")
                else:
                    # raise Exception("processor ws is not running")
                    print("\n-------------------- : processor_ws is not connect : ------------------------------")
                    # 07 check exsist
                    handlers.users_ws_connections[tempUser_objectId] = {
                        "processor_objectId": tempUser_model.processor_info.processor_ObjectId,
                        "websocket": websocket,
                        "user_objectId": tempUser_objectId,
                        "phoneApp_dic": TempUser_utils.get_tempPhoneAppDic_from_tempUser_model(tempUser_model),
                        "onlineApp_dic" : {}
                    }
                    try:
                        while websocket.open:
                            data = yield from websocket.recv()
                            if not data:
                                print("\n----- : tempUser_websocket.recv() : not data : -----------")
                                continue
                            logger.debug(data)
                            print("client : data == " + str(data))
                            # as temp truing
                            # main_tag_handler(data)

                            try:
                                # yield from router.MessageRouter(data)()
                                # as temp for temp user
                                # temp user uses original user router
                                yield from TempUser_router.TempUserRequestRouter(data, tempUser_objectId)()
                                pass
                            except Exception as e:
                                logger.error('could not route msg', e)

                    except websockets.exceptions.InvalidState:  # User disconnected
                        pass
                    finally:
                        #del tempUsers_ws_connections[tempUser_objectId]
                        del handlers.users_ws_connections[tempUser_objectId]
                        print("\n----------------- Temp User Closing -------------------------")
    else:
        raise Exception("tempUser model is not exist")


