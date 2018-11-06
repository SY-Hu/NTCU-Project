from twilio.rest import Client

account_sid = "AC17b9c6052ec5171f65eb484be72df9de"
auth_token = "eef3987b76d7ca85edda83d5a8e8a756"

client = Client(account_sid, auth_token)

message = client.messages.create(
        "+8860978912385",
        body="Test meaasge to SY-Hu !",
        from_="+14437072667"
)

print(message.sid)