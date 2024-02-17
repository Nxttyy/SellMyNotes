import http.client
import json, uuid

conn = http.client.HTTPSConnection("api.chapa.co")

def handle_chappa(amount, email, first_name, phone_number, title, return_url):
  
  phone_number = str(phone_number).replace('-', '')

  payload = json.dumps({
    "amount": str(amount),
    "currency": "ETB",
    "email": str(email),
    "first_name": "Bilen",
    "phone_number": phone_number,
    "tx_ref": str(uuid.uuid4().hex),
    "callback_url": "https://webhook.site/077164d6-29cb-40df-ba29-8a00e59a7e60",
    "return_url": "http://127.0.0.1:5000/"+return_url,
    "customization[title]": str(email),
    "customization[description]": "I love online payments"
  })
  headers = {
    'Authorization': 'Bearer CHASECK_TEST-zOmNpkdcH4CnZ23gGYIg3IeNxtolil24',
    'Content-Type': 'application/json'
  }

  return conn, payload, headers
  # res = conn.getresponse()
  # data = res.read()
  # print(data.decode("utf-8"))


# import http.client
# import json

# conn = http.client.HTTPSConnection("api.chapa.co")
# payload = json.dumps({
#   "amount": "100",
#   "currency": "ETB",
#   "email": "abebech_bekele@gmail.com",
#   "first_name": "Bilen",
#   "last_name": "Gizachew",
#   "phone_number": "0912345678",
#   "tx_ref": "chewatssatest-6669",
#   "callback_url": "https://webhook.site/077164d6-29cb-40df-ba29-8a00e59a7e60",
#   "return_url": "https://www.google.com/",
#   "customization[title]": "Payment for my favourite merchant",
#   "customization[description]": "I love online payments"
# })
# headers = {
#   'Authorization': 'Bearer CHASECK_TEST-zOmNpkdcH4CnZ23gGYIg3IeNxtolil24',
#   'Content-Type': 'application/json'
# }
# conn.request("POST", "/v1/transaction/initialize", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))