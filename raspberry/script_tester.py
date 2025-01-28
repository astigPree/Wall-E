from my_tools import *
import time
import rules
 
# data = send_post_request()
# if data:
#     print(f"Received data: {data}")
 
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




from pyuac import main_requires_admin

@main_requires_admin
def main():
    print("Do stuff here that requires being run as an admin.")
    # The window will disappear as soon as the program exits!
    # input("Press enter to close the window. >")
  
    import serial
    import time

    arduino = serial.Serial(port='COM5',  baudrate=115200, timeout=.1)


    def write_read(x):
        arduino.write(bytes(x,  'utf-8'))
        time.sleep(0.05)
        data = arduino.readline()
        return  data


    while True:
        num = input("Enter a number: ")
        value  = write_read(num)
        print(value)

main()

