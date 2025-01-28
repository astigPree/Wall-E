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



from aitextgen import aitextgen

# Without any parameters, aitextgen() will download, cache, and load the 124M GPT-2 "small" model
ai = aitextgen()

ai.generate()
ai.generate(n=3, max_length=100)
ai.generate(n=3, prompt="I believe in unicorns because", max_length=100)
ai.generate_to_file(n=10, prompt="I believe in unicorns because", max_length=100, temperature=1.2)


