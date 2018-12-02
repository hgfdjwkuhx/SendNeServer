from SendNeSocketsApp.management.StoreModel.StorePeeWee.ReceiverPrivateStoreManager.PrivateStoreModel import \
    ReceiverRequestsPrivateStoreModel

storeModel = ReceiverRequestsPrivateStoreModel()









if __name__ == '__main__':

    handle_requests = storeModel.UserProcessorHandleRequest.filter(
        (storeModel.UserProcessorHandleRequest.processor_objectId == "jptkadqolfubyglqedtcrqfuwuakbotperaggepanaeorrbcesayzyoqvymq") &
        (storeModel.UserProcessorHandleRequest.request_state == storeModel.HandleRequestState.JustAdd)

                                                                   )
    handle_requests_list = list(handle_requests)
    print("\nhandle_requests length == " + str(handle_requests.__len__()))
    print(str(handle_requests_list))



















