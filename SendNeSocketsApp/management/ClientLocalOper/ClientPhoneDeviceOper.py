from SendNeSocketsApp.Commons.BlockStates import BlockedStatu
from SendNeSocketsApp.management.ErrorsClientMessages.ClientPhoneDeviceMessages import ClientPhoneDeviceMessage
from SendNeSocketsApp import models



def new_phone_device(userObjectId , packet):

    userPrivate_model = None
    if type(userObjectId) is not str :
        raise Exception("error in userObjectId type")

    if userObjectId.__len__() == 42:
        # is user
        try:
            userPrivate_model = models.UserPrivateProcessorInfo.objects.get(user_objectId=userObjectId)
        except:
            raise Exception("error in userObjectId is not exist")
            #userPrivate_model = None

        count_avali = userPrivate_model.related_phone_device_private_user_info.filter(device_state=models.PhoneDevicePrivateUserInfo.DeviceState.Available).count()

        #here as temp
        if count_avali > 5 :
            return ClientPhoneDeviceMessage.Have_Maximum_Phones_Devices(packet.get("device_objectId"))
        else:
            device_objectId = packet.get("device_objectId")

            dev_model = models.PhoneDevicePrivateUserInfo()
            dev_model.user_private_processor_objectId = userObjectId
            dev_model.device_name = packet.get("device_name")
            dev_model.client_objectId = packet.get("device_objectId")
            dev_model.user_private_processor = userPrivate_model

            dev_model.device_state = models.PhoneDevicePrivateUserInfo.DeviceState.Available
            dev_model.blocked_state = BlockedStatu.Running


            try:
                dev_model.save()
                return {
                    "type-content": "notify",
                    "notify": "sys",
                    "tag": "device",
                    "type-device": "devices_detail",
                    "result": {
                        "statu": "done",
                        "device_info": dev_model.get_InfoDic_clinet()
                    }
                }
            except:
                return ClientPhoneDeviceMessage.Error_In_Save(packet.get("device_objectId"))

    else:
        if userObjectId.__len__() == 65:
            # is temp user
            try:
                userPrivate_model = models.TempUserPrivateProcessorInfo.objects.get(user_objectId=userObjectId)
            except:
                raise Exception("error in userObjectId is not exist")
                # userPrivate_model = None

            count_avali = userPrivate_model.related_temp_phone_device_private_user_info.filter(
                device_state=models.TempPhoneDevicePrivateUserInfo.DeviceState.Available).count()

            # here as temp
            if count_avali > 2:
                return ClientPhoneDeviceMessage.Have_Maximum_Phones_Devices(packet.get("device_objectId"))
            else:
                device_objectId = packet.get("device_objectId")

                dev_model = models.TempPhoneDevicePrivateUserInfo()
                dev_model.temp_user_private_processor_objectId = userObjectId
                dev_model.device_name = packet.get("device_name")
                dev_model.client_objectId = packet.get("device_objectId")
                dev_model.temp_user_private_processor = userPrivate_model

                dev_model.device_state = models.TempPhoneDevicePrivateUserInfo.DeviceState.Available
                dev_model.blocked_state = BlockedStatu.Running

                try:
                    dev_model.save()
                    return {
                        "type-content": "notify",
                        "notify": "sys",
                        "tag": "device",
                        "type-device": "devices_detail",
                        "result": {
                            "statu": "done",
                            "device_info": dev_model.get_InfoDic_clinet()
                        }
                    }
                except:
                    return ClientPhoneDeviceMessage.Error_In_Save(packet.get("device_objectId"))


def infoAll_phone_device(userObjectId , packet):

    userPrivate_model = None
    if type(userObjectId) is not str :
        raise Exception("error in userObjectId type")

    if userObjectId.__len__() == 42:
        try:
            userPrivate_model = models.UserPrivateProcessorInfo.objects.get(user_objectId=userObjectId)
        except:
            raise Exception("error in userObjectId is not exist")
            #userPrivate_model = None

        count_avali = userPrivate_model.related_phone_device_private_user_info.filter(device_state=models.PhoneDevicePrivateUserInfo.DeviceState.Available)

        device_info_list = []

        for modell in count_avali:
            device_info_list.append(modell.get_InfoDic_clinet())

        return {
            "type-content": "notify",
            "notify": "sys",
            "tag": "device",
            "type-device": "devices_detail",
            "result": {
                "statu": "done",
                "devices_info": device_info_list
            }
        }

    else:
        if userObjectId.__len__() == 65:
            # is temp user
            try:
                userPrivate_model = models.TempUserPrivateProcessorInfo.objects.get(user_objectId=userObjectId)
            except:
                raise Exception("error in temp userObjectId is not exist")
                # userPrivate_model = None

            count_avali = userPrivate_model.related_temp_phone_device_private_user_info.filter(
                device_state=models.TempPhoneDevicePrivateUserInfo.DeviceState.Available)

            device_info_list = []

            for modell in count_avali:
                device_info_list.append(modell.get_InfoDic_clinet())

            return {
                "type-content": "notify",
                "notify": "sys",
                "tag": "device",
                "type-device": "devices_detail",
                "result": {
                    "statu": "done",
                    "devices_info": device_info_list
                }
            }
        else:
            raise Exception("error in userObjectId length")



