import requests
import xmltodict

URL = "https://www.biblegateway.com/votd/get/"

response = requests.get(URL)
data = xmltodict.parse(response.content)
votd_text = data["votd"]["content"] + " | " + data["votd"]["reference"]

print(votd_text)
