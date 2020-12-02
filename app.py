# Copyright © 2020 Cezar Popoveniuc
# Free to use for any purpose
# Custom software, not in association with Adservio in any way shape or form
import PySimpleGUI as GUI
import requests
from playsound import playsound

info_session_number = 0
session_number = 0
incorrect_credentials_session_number = 0

main_layout = [[GUI.Text("Main page", justification='center')], [GUI.Text("Adservio Username")], [GUI.InputText()], [GUI.Text("Adsevio Password")], 
    [GUI.InputText()], [GUI.Button("Exit"), GUI.Button("Start")], [GUI.Button("Press for more information")]]
uaID = ''
session_cookie = ''
def play_alarm():
    alarm_layout = [[GUI.Text("Alarma", justification='center')], [GUI.Button("STOP")]]
    alarm_window = GUI.Window(title = "Alarma", layout=alarm_layout, margins=(100, 50))
    while True:
        event_alarm, value_alarm = alarm_window.read(50)
        if event_alarm == GUI.WIN_CLOSED or event_alarm == 'STOP':
            break
        else:
            playsound('Alarm_short.mp3')
    alarm_window.close()

def session_response(session):
    #FIRST REQUEST
    burp0_url = "https://www.adservio.ro:443/ro/messages"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1", "If-Modified-Since": "Fri, 27 Nov 2020 15:55:04 GMT", "Cache-Control": "max-age=0"}
    session.get(burp0_url, headers=burp0_headers)

    #SECOND REQUEST

    burp0_url = "https://www.adservio.ro:443/api/v2/auth/accounts?uaID="+uaID
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Authorization": "Bearer " + session_cookie, "X-App-Version": "web 1.0", "Connection": "close", "Referer": "https://www.adservio.ro/ro/messages", "Cache-Control": "max-age=0"}
    session.get(burp0_url, headers=burp0_headers)

    #THIRD REQUEST

    burp0_url = "https://www.adservio.ro:443/api/v2/mesaje?msgType=1&filterSearch=&filterUaTip=&_offset=0&_limit=15"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Authorization": "Bearer " + session_cookie, "X-App-Version": "web 1.0", "Connection": "close", "Referer": "https://www.adservio.ro/ro/messages", "Cache-Control": "max-age=0"}
    Response = session.get(burp0_url, headers=burp0_headers)

    return Response.text
    #FOURTH REQUEST

    burp0_url = "https://www.adservio.ro:443/api/v2/mesaje?msgType=1&filterSearch=&filterUaTip=&_offset=0&_limit=15"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Authorization": "Bearer " + session_cookie, "X-App-Version": "web 1.0", "Connection": "close", "Referer": "https://www.adservio.ro/ro/messages"}
    session.get(burp0_url, headers=burp0_headers)


def run_app(session):
    global session_number
    session_number = session_number + 1
    layout_for_now = [[GUI.Text("App is running")], [GUI.Text('Session ' + str(session_number))], [GUI.Button("Manual Refresh")], [GUI.Button("Cancel")]]

    window_app = GUI.Window(title="App is running", layout=layout_for_now, margins=(100, 50))

    Response = session_response(session)
    
    while True:
        event_app, value_app = window_app.read(timeout=2000)
        if event_app == 'Cancel' or event_app == GUI.WIN_CLOSED:
            break
        
        Response2 = session_response(session)

        if Response != Response2:
            play_alarm()
            break
    
    window_app.close()

def more_infomation():
    global info_session_number
    info_session_number = info_session_number + 1
    layout_more_info =  [[GUI.Text("How to use")], [GUI.Text("Enter your Adservio username and password.")],
    [GUI.Text("You will hear an alarm when a message arrives.")], [GUI.Text("After pressing 'Start' check in your browser if the message hadn't already arrived.")],
    [GUI.Text("Warning!!! Reading an unread message or deleting a message while the app is running also triggers the alarm.")],
    [GUI.Text("You clicked on more info " + str(info_session_number) + " times.")], [GUI.Button("Back")]]
    window_info = GUI.Window(title="More info", layout=layout_more_info, margins=(100, 50))
    while True:
        events_info, values_info = window_info.read()
        if events_info == GUI.WIN_CLOSED or events_info == "Back":
            break
    window_info.close()

def incorrect_credentials_window():
    global incorrect_credentials_session_number
    incorrect_credentials_session_number = incorrect_credentials_session_number + 1
    layout_incorrect_creds = [[GUI.Text("The credentials you entered are incorrect")], [GUI.Text("This is the " + str(incorrect_credentials_session_number) 
    + " time")], [GUI.Button("Back")]]
    window_incorrect_creds = GUI.Window(title="Incorrect credentials", layout=layout_incorrect_creds, margins=(100, 50))
    while True:
        event_incorrect_creds, values_incorrect_creds = window_incorrect_creds.read()
        if event_incorrect_creds == GUI.WIN_CLOSED or event_incorrect_creds == "Back":
            break
    window_incorrect_creds.close()

def verify_credentials(username, password):

    session = requests.Session()
    URL = "https://www.adservio.ro:443/api/v2/utilizatori/profile_username?uaUserName=" + username
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "application/json, text/plain, */*", 
    "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Referer": "https://www.adservio.ro/ro"}
    Response = session.get(URL, headers=header)
    print("Username request response:")
    print(Response.text)
    if 'Invalid' in Response.text or 'error' in Response.text:
        return 0
    

    burp0_url = "https://www.adservio.ro:443/api/v2/auth"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "multipart/form-data; boundary=---------------------------15246821746248209312605927681", "Origin": "https://www.adservio.ro", "Connection": "close", "Referer": "https://www.adservio.ro/ro"}
    burp0_data = "-----------------------------15246821746248209312605927681\r\nContent-Disposition: form-data; name=\"intent\"\r\n\r\nauth\r\n-----------------------------15246821746248209312605927681\r\nContent-Disposition: form-data; name=\"uaUserName\"\r\n\r\n"+username+"\r\n-----------------------------15246821746248209312605927681\r\nContent-Disposition: form-data; name=\"uaPassword\"\r\n\r\n"+password+"\r\n-----------------------------15246821746248209312605927681\r\nContent-Disposition: form-data; name=\"tfaOptID\"\r\n\r\n\r\n-----------------------------15246821746248209312605927681\r\nContent-Disposition: form-data; name=\"tfaResponse\"\r\n\r\nundefined\r\n-----------------------------15246821746248209312605927681\r\nContent-Disposition: form-data; name=\"tfaSave\"\r\n\r\nfalse\r\n-----------------------------15246821746248209312605927681\r\nContent-Disposition: form-data; name=\"uaNewPassword\"\r\n\r\n\r\n-----------------------------15246821746248209312605927681\r\nContent-Disposition: form-data; name=\"uaNewPassword2\"\r\n\r\n\r\n-----------------------------15246821746248209312605927681\r\nContent-Disposition: form-data; name=\"setCookie\"\r\n\r\n1\r\n-----------------------------15246821746248209312605927681--\r\n"                                                                             
    Response = session.post(burp0_url, headers=burp0_headers, data=burp0_data)

    print("Password request response:")
    print(Response.text)
    if 'Invalid' in Response.text or 'error' in Response.text:
        return 0
    
    global session_cookie
    global uaID
    uaID = Response.text.split('uaID')[1]
    uaID = uaID.split(":")[1].split('"')[1].split('"')[0]

    session_cookie = str(Response.headers).split('ADST=')[1].split(';')[0]
    print("Session Cookie")
    print(session_cookie)
    return session

def main():
    window = GUI.Window(title="Adservio App", layout=main_layout, margins=(100,50))
    while True:
        event, values = window.read()
        if event == "Exit" or event == GUI.WIN_CLOSED:
            exit(0)
        elif event == 'Press for more information':
            more_infomation()
        elif event == 'Start':
            username = values[0]
            password = values[1]
            sesiune = verify_credentials(username, password)
            if isinstance(sesiune, int):
                incorrect_credentials_window()
            else:
                run_app(sesiune)
    window.close()
if __name__ == "__main__":
    main()