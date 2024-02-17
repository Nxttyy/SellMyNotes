# from handle_payment import handle_chappa

# conn, payload, headers = handle_chappa("200", "try@gmail.com", "first_name", "0900123456"
# , "Title", "www.google.com")
# # print(conn, headers)
# res = conn.request("POST", "/v1/transaction/initialize", payload, headers)
# print(res)

# redirect_url = res.get("data").get("checkout_url")
# print(redirect_url)

import http.client
import json, uuid

conn = http.client.HTTPSConnection("api.chapa.co")

def handle_chappa():
  
    # phone_number = str(phone_number).replace('-', '')

    payload = json.dumps({
    "amount": "200",
    "currency": "ETB",
    "email": "try@gmail.com",
    "first_name": "Bilen",
    "phone_number": "0900123456",
    "tx_ref": str(uuid.uuid4().hex),
    "callback_url": "https://webhook.site/077164d6-29cb-40df-ba29-8a00e59a7e60",
    "return_url": "http://127.0.0.1:5000/",
    "customization[title]": "Title",
    "customization[description]": "I love online payments"
    })
    headers = {
    'Authorization': 'Bearer CHASECK_TEST-zOmNpkdcH4CnZ23gGYIg3IeNxtolil24',
    'Content-Type': 'application/json'
    }

    conn.request("POST", "/v1/transaction/initialize", payload, headers)
    print(conn.getresponse().read())

    redirect_url = res.get("data").get("checkout_url")
    print(redirect_url)

handle_chappa()
