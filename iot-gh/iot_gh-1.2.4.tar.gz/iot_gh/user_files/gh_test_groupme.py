import time
from iot_gh.IoTGreenhouseService import IoTGreenhouseService
from iot_gh.GHTextingService import GHTextingService

def main():
    ghs = IoTGreenhouseService()

    ACCESS_TOKEN = ""
    ACCESS_TOKEN = input("Please enter your dev.groupme.com access token: ").strip()
    t_service = GHTextingService(ACCESS_TOKEN, ghs,"iot_gh_testing")

    last_message_id = None;
    while True:
        if t_service.last_message != None:
            if t_service.last_message.id != last_message_id:
                name = t_service.last_message.name
                text = t_service.last_message.text
                print(name + "   " + text)
                print()

                last_message_id = t_service.last_message.id
            time.sleep(1)
              
    
if __name__ == "__main__":
    main()