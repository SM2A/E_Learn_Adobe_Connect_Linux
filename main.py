import time
import urllib3
import getpass
import requests
import webbrowser
from bs4 import BeautifulSoup

urllib3.disable_warnings()

URL = 'https://elearn.ut.ac.ir/'
session_req = requests.session()

print('Hi')

username = input('Username: ')
password = getpass.getpass(prompt='Password: ')
# password = input('Password: ')
address = input('Course Online Room Entry Page: ')

login_request = None

while True:
    try:
        login_request = requests.get(URL, verify=False)
        break
    except:
        error = 0
        print('Error')
        time.sleep(10)

result = session_req.get(login_request.url, verify=False)
encoding = result.encoding
parser = BeautifulSoup(result.text, "html.parser")
execution = parser.find("input", type="hidden")["value"]

post_data = {'username': username, 'password': password, 'execution': execution,
             '_eventId': 'submit', 'submit': 'LOGIN', 'geolocation': ''}

login_result = session_req.post(login_request.url, data=post_data, headers=dict(refer=login_request.url), verify=False)
result = None
while True:
    try:
        result = session_req.get(address)
        break
    except:
        error = 0
        print('Error')
        time.sleep(10)

content_parse = BeautifulSoup(result.text, "html.parser")
content = content_parse.find('input', {"value": "پيوستن به كلاس"})
link = content.attrs.get('onclick')

room_session = ""
ses = False
index = str(link).find('sesskey')
while index != len(str(link)):
    index += 1
    if str(link)[index] == '&':
        break
    if str(link)[index] == '=':
        ses = True
        continue
    if ses:
        room_session += str(link)[index]

# print(room_session)

index = 0
quote_count = 0
vclass_link = ""

while index != len(str(link)):
    index += 1
    if str(link)[index] == '\'':
        quote_count += 1
        index += 1
    if quote_count == 2:
        break
    if quote_count == 1:
        vclass_link += str(link)[index]

# print(vclass_link)

while True:
    try:
        result = session_req.get(vclass_link)
        break
    except:
        error = 0
        print('Error')
        time.sleep(10)


# print(result.url + '&proto=true')

webbrowser.open(result.url + '&proto=true')
