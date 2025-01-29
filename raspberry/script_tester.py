from my_tools import *
import time
import rules
 
data = send_post_request()
if data:
    print(f"Received data: {data}")
 
data = {
    'patients': {
        '8': {
            'id': 8,
            'name': 'Arthur A. Arthur',
            'first_name': 'Arthur',
            'last_name': 'Arthur',
            'middle_name': 'Arthur',
            'date_added': '2025-01-19 06:16:02',
            'face': '/media/patient_faces/patient_image_j5Gr6Tu.jpg'
        }
    },
    'nurses': {
        '3': {
            'id': 3,
            'name': 'Joy T. Tarucan',
            'first_name': 'Joy',
            'last_name': 'Tarucan',
            'middle_name': 'Tambak',
            'date_added': '2025-01-19 07:00:38',
            'face': '/media/nurse_faces/nurse_image.jpg'
        }
    },
    'schedules': {
        '9': {
            'id': 9,
            'nurse': None,
            'patient': 8,
            'created_at': '2025-01-19 00:00:00',
            'pill': 'Citirizine',
            'is_daily': False,
            'is_medication_taken': False,
            'set_date': '2025-01-15',
            'set_time': '12:38'
        }
    }
}


# from aitextgen import aitextgen

# # Without any parameters, aitextgen() will download, cache, and load the 124M GPT-2 "small" model
# ai = aitextgen()

# # ai.generate()
# # ai.generate(n=3, max_length=100)
# generate = ai.generate_one(prompt="hello guys", max_length=1000)
# print("================================================")
# print(generate)




# from pyuac import main_requires_admin

# @main_requires_admin
# def main():
#     print("Do stuff here that requires being run as an admin.")
#     # The window will disappear as soon as the program exits!
#     # input("Press enter to close the window. >")
  
#     import serial
#     import time

#     arduino = serial.Serial(port='COM5',  baudrate=115200, timeout=.1)


#     def write_read(x):
#         arduino.write(bytes(x,  'utf-8'))
#         time.sleep(0.05)
#         data = arduino.readline()
#         return  data


#     while True:
#         num = input("Enter a number: ")
#         value  = write_read(num)
#         print(value)

# main()



# *- coding: utf-8 -*-
# send_txt_msg.py
# 04-02-2021 03:08:34 EDT
# (c) 2021 acamso

"""Sends TXT message with GMail.

This is a demonstration on how to send an text message with Python.
In this example, we use GMail to send the SMS message,
but any host can work with the correct SMTP settings.
Each carrier has a unique SMS gateway hostname.
This method is completely free and can be useful in a variety of ways.

Video: https://youtu.be/hKxtMaa2hwQ
Turn on: https://myaccount.google.com/lesssecureapps
"""

import asyncio
import re
from email.message import EmailMessage
from typing import Collection, List, Tuple, Union

import aiosmtplib

HOST = "smtp.gmail.com"
# https://kb.sandisk.com/app/answers/detail/a_id/17056/~/list-of-mobile-carrier-gateway-addresses
# https://www.gmass.co/blog/send-text-from-gmail/
CARRIER_MAP = {
    "verizon": "vtext.com",
    "tmobile": "tmomail.net",
    "sprint": "messaging.sprintpcs.com",
    "at&t": "txt.att.net",
    "boost": "smsmyboostmobile.com",
    "cricket": "sms.cricketwireless.net",
    "uscellular": "email.uscc.net",
}


# pylint: disable=too-many-arguments
async def send_txt(
    num: Union[str, int], carrier: str, email: str, pword: str, msg: str, subj: str
) -> Tuple[dict, str]:
    to_email = CARRIER_MAP[carrier]

    # build message
    message = EmailMessage()
    message["From"] = email
    message["To"] = f"{num}@{to_email}"
    message["Subject"] = subj
    message.set_content(msg)

    # send
    send_kws = dict(username=email, password=pword, hostname=HOST, port=587, start_tls=True)
    res = await aiosmtplib.send(message, **send_kws)  # type: ignore
    print(res)
    msg = "failed" if not re.search(r"\sOK\s", res[1]) else "succeeded"
    print(msg)
    return res


async def send_txts(
    nums: Collection[Union[str, int]], carrier: str, email: str, pword: str, msg: str, subj: str
) -> List[Tuple[dict, str]]:
    tasks = [send_txt(n, carrier, email, pword, msg, subj) for n in set(nums)]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    _num = "09279121857"
    _carrier = "verizon"
    _email = "vincelance62@gmail.com"
    _pword = "ozoxahnrfrsdaerj"
    _msg = "Dummy msg"
    _subj = "Dummy subj"
    coro = send_txt(_num, _carrier, _email, _pword, _msg, _subj)
    # _nums = {"999999999", "000000000"}
    # coro = send_txts(_nums, _carrier, _email, _pword, _msg, _subj)
    try:
        
        asyncio.run(coro)
    except Exception as e:
        print(f"An error occurred: {e}")
    except RuntimeError as e:
        print(f"An error occurred: {e}")




import requests

resp = requests.post('https://textbelt.com/text', {
  'phone': '09512213008',
  'message': 'Hello world',
  'key': 'textbelt',
})
print(resp.json())