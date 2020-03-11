from signalwire.rest import Client as signalwire_client

client = signalwire_client("YourProjectID", "YourAuthToken", signalwire_space_url = 'example.signalwire.com')

message = client.messages.create(
                              from_='+15551234567',
                              body='Hello World!',
                              to='+15557654321'
                          )

print(message.sid)
