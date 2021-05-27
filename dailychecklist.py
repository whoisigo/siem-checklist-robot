# =======================================================================
#                                                                    
#   Author: Igor Nobre                         
#   Date: 10-17-2020                                                   
#   Description: Automate a SIEM Team health check routine         
#   Last update:                                                          
#   Example: python3 ./dailyChecklist.py                              
#                                                                          
# =======================================================================

import webbrowser, pyautogui, requests, smtplib, time, os 
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from datetime import date

#Lists & variable
maps = [
#Insert URLs which will be monitored
  'https://grafana.example.com.br/page01', 
  'https://zabbix.example.com.br/page02' 

#Path
path_screenshot = ('C:\\Users\\youruser\\Documents\\Scripts\\Diversos\\Python\\Print\\')
#Week day
now = date.today().strftime("Day %d of %B of %Y, week %V")

#SMTP Settings (Relay)
receiver = 'your teams e-mail channel'
pwwd = 'password'
server = smtplib.SMTP('smtp.gmail.com', 25)
sender = 'your sender e-mail'

#1 Get checklist url's
def openUrls():
  for x in range(len(maps)):
    webbrowser.open(maps[x], new=1)
    time.sleep(10)
    sc = pyautogui.screenshot(region=(0,250, 1200, 600))
    sc.save(f'{path_screenshot}{x}.png')
  #os.system('taskkill /F /IM msedge.exe > null')           

#2 Send e-mail to teams channel 
def sendEmail():
  msg = MIMEMultipart()
  msg['Subject'] = (f'[Performance Indicators | {now}]\n')
  msg['From'] = sender
  msg['To'] = receiver
  msgAlternative = MIMEMultipart('alternative')
  msg.attach(msgAlternative)

  #Capture images to compose an email notify
  for i in range(4):
    time.sleep(1)
    ft = open(f'{path_screenshot}{i}.png', 'rb')
    image = MIMEImage(ft.read())
    image.add_header('Content-ID', f'<image{i}>')
    msg.attach(image)
    ft.close()

  msgText = MIMEText('''\
            <br><img src="cid:image0">
            <img src="cid:image1">
            <img src="cid:image2">
            <img src="cid:image3">

            <br>Best Regards,</br>
            Cyber Security Team
            ''', 'html')  
  msgAlternative.attach(msgText)
  
  #Conf outlook
  #server.sendmail(sender, receiver, out.as_string())
  
  #Conf gmail
  server.starttls()
  server.login(sender, pwwd)
  server.sendmail(sender, receiver, msg.as_string())
  server.quit()

#3 Remove images
def removeImg():
    test = os.listdir(path_screenshot)
    for item in test: 
        if item.endswith('.png'):
            os.chdir(path_screenshot)
            os.remove(item)
        else:
            continue    

#4 Beggin & validation
url = requests.get(maps[0])
if url.status_code == 200:
    openUrls()
    time.sleep(10)
    sendEmail()
    time.sleep(15)
    removeImg()
    
else:
    out = '*** ERROR *** Something is wrong while attempt to connect to one or more URLs'
    server.starttls()
    server.login(sender, pwwd)
    server.sendmail(sender, receiver, out.encode('utf8'))
    server.quit()
