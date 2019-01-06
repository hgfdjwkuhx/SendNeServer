from SendNeSocketsApp import models



def get_TempPhoneDeviceInfo_from_session(session_key):
    # main_TempUserProcessorInfo_Lock.acquire()

    phone_model = models.TempPhoneDevicePrivateUserInfo.objects.get(temp_token=session_key)
    if phone_model is not None:
        return phone_model
    else:
        raise Exception("temp_phone_model model is not exist")
        #return None
    # main_TempUserProcessorInfo_Lock.release()




