from my_tools import *
import time
import rules

# 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




from speech_recognition_utils import SpeechRecognitionUtils

recognizer = SpeechRecognitionUtils()
while True:
    text = recognizer.recognize_speech()
    print(f"Text received: {text}")
    
    









# from voice_utils import VoiceUtils

# voice = VoiceUtils()

# voice.speak("Hello There! Could you repeat your request because i did not understand the message")  








# data = send_post_request()
# if data:
#     print(f"Received data: {data}")
 
# data = {
#     'patients': {
#         '8': {
#             'id': 8,
#             'name': 'Arthur A. Arthur',
#             'first_name': 'Arthur',
#             'last_name': 'Arthur',
#             'middle_name': 'Arthur',
#             'date_added': '2025-01-19 06:16:02',
#             'face': '/media/patient_faces/patient_image_j5Gr6Tu.jpg'
#         }
#     },
#     'nurses': {
#         '3': {
#             'id': 3,
#             'name': 'Joy T. Tarucan',
#             'first_name': 'Joy',
#             'last_name': 'Tarucan',
#             'middle_name': 'Tambak',
#             'date_added': '2025-01-19 07:00:38',
#             'face': '/media/nurse_faces/nurse_image.jpg'
#         }
#     },
#     'schedules': {
#         '9': {
#             'id': 9,
#             'nurse': None,
#             'patient': 8,
#             'created_at': '2025-01-19 00:00:00',
#             'pill': 'Citirizine',
#             'is_daily': False,
#             'is_medication_taken': False,
#             'set_date': '2025-01-15',
#             'set_time': '12:38'
#         }
#     }
# }


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
# import serial
# import time
# from arduino_connection import ArduinoConnection

# arduino = ArduinoConnection()
# arduino.initialized(port='/dev/ttyACM0', baudrate=115200)

# # arduino = serial.Serial(port='COM4', baudrate=115200, timeout=0.1)

# # def write_data(x):
# #     arduino.write(bytes(x + '\n', 'utf-8'))

# # def read_data():
# #     data = arduino.readline().decode('utf-8').rstrip()
# #     return data

# while True:
#     command = input("Enter command (ON/OFF): ")
#     arduino.write(command)
#     # write_data(command)
#     time.sleep(2)
#     value = arduino.read()
#     print(value)
#     time.sleep(1)
#     value = arduino.read()
#     print(value)



# }

# *- coding: utf-8 -*-
# send_txt_msg.py
# 04-02-2021 03:08:34 EDT
# (c) 2021 acamso 
# from PIL import Image
# import imagehash

# hash = imagehash.average_hash(Image.open('images/patient_faces/WIN_20250129_23_40_36_Pro.jpg'))
# otherhash = imagehash.average_hash(Image.open('WIN_20250130_00_36_22_Pro.jpg'))
# otherhash2 = imagehash.average_hash(Image.open('images/patient_faces/patient_image_YnA6FjE.jpg'))
# otherhash3 = imagehash.average_hash(Image.open('WIN_20250130_00_40_25_Pro.jpg'))
# otherhash4 = imagehash.average_hash(Image.open('WIN_20250130_00_41_12_Pro.jpg')) 
# otherhash5 = imagehash.average_hash(Image.open('WIN_20250130_00_42_47_Pro.jpg')) 
# otherhash6 = imagehash.average_hash(Image.open('WIN_20250130_00_44_12_Pro.jpg')) 
# otherhash7 = imagehash.average_hash(Image.open('WIN_20250130_00_44_43_Pro.jpg')) 


# print(hash == otherhash)
# print(hash - otherhash)
# print(hash == otherhash2)
# print(hash - otherhash2)
# print(hash == otherhash3)
# print(hash - otherhash3)

# print(hash == otherhash4)
# print(hash - otherhash4)

# print(hash == otherhash5)
# print(hash - otherhash5)

# print(hash == otherhash6)
# print(hash - otherhash6)

# print(hash == otherhash7)
# print(hash - otherhash7)








# import cv2
# from PIL import Image
# import imagehash
# from imagededup.methods import PHash
# phasher = PHash()

# encodings = phasher.encode_images(image_dir='images/patient_faces/')

# def open_camera_and_hash_image():
#     # Open the camera
#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         return

#     # Capture a frame
#     ret, frame = cap.read()

#     if not ret:
#         print("Error: Could not read frame.")
#         return

#     # Convert the frame from BGR to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Convert the frame to PIL Image
#     pil_image = Image.fromarray(rgb_frame)

#     # Compute the hash of the captured frame
#     frame_hash = imagehash.average_hash(pil_image)

#     # Print the hash
#     print("Hash of captured frame:", frame_hash)
#     hash = imagehash.average_hash(Image.open('images/patient_faces/patient_image_j5Gr6Tu.jpg'))
#     print(hash == frame_hash)
#     print(hash - frame_hash)

#     # Release the camera
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     open_camera_and_hash_image()





# # from speech_recognition_utils import SpeechRecognitionUtils
# # recognizer = SpeechRecognitionUtils()


# # while True:
# #     text = recognizer.recognize_speech()
# #     print(f"Text received: {text}")



# import subprocess

# pt = subprocess.Popen(['/opt/vc/bin/vcgencmd', 'get_throttled'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# (res,err) = pt.communicate()
# res = res.decode().split("=")[1]
# res = res.rstrip("\n")
# print ("Current Power Issues?    = ",(int(res,0) & 0x01) == 0x01)
# print ("Any Power issues before? = ",(int(res,0) & 0x50000) == 0x50000)