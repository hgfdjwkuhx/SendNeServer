

class ClientPhoneDeviceMessage:

    @staticmethod
    def Have_Maximum_Phones_Devices(device_objectId):
        return {
            "type-content": "notify",
            "notify": "sys",
            "tag" : "device",
            "type-device" : "error_msg",
            "result" : {
                "type-error": "maximum_devices",
                "message_showing": "you have maximum of phones devices",
                "device_objectId": str(device_objectId)
            }
        }

    @staticmethod
    def Error_In_Save(device_objectId):
        return {
            "type-content": "notify",
            "notify": "sys",
            "tag" : "device",
            "type-device" : "error_msg",
            "result" : {
                "type-error": "trying",
                "message_showing": "try create new phone later !!",
                "device_objectId": str(device_objectId)
            }
        }