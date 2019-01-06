from SendNeSocketsApp import models
from SendNeSocketsApp.Commons.BlockStates import BlockedStatu


def get_tempUserProcessorInfo_from_session(session_key):
    # main_TempUserProcessorInfo_Lock.acquire()
    tempUser_model = models.TempUserPrivateProcessorInfo.objects.get(temp_token=session_key)
    if tempUser_model is not None:
        return tempUser_model
    else:
        raise Exception("tempUser model is not exist")
        #return None
    # main_TempUserProcessorInfo_Lock.release()


def set_Processor_For_tempUserInfo(tempUser_model):
    # this as temp
    tempUser_model.processor_info = models.ProcessorInfo.objects.first()
    if tempUser_model.processor_info is None:
        raise Exception("tempUser processor_info is null")
    else:
        tempUser_model.blocked_state = BlockedStatu.Running
        tempUser_model.save()



def get_tempPhoneAppDic_from_tempUser_model(user_model):
    #user_model = models.TempUserPrivateProcessorInfo()

    phoneApps_model = user_model.related_temp_phone_device_private_user_info.filter(blocked_state=BlockedStatu.Running)
    apps_dic = {}
    for app_model in phoneApps_model:
        apps_dic[app_model.client_objectId] = app_model.self_objectId

    return apps_dic

