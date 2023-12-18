from twilio.rest import Client

class Phone:
    def __init__(self, phoneNumber: str, acc_sid: str, auth_token: str):
        self.__phoneNumber = f"+1{phoneNumber}"
        self.__client = Client(acc_sid, auth_token)
    
    def sendSMS(self, message: str) -> None:
        self.__client.messages.create(
            to=self.__phoneNumber,
            from_="+18557842852",
            body=message)
    
    