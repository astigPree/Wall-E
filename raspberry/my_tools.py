


import json
import re
import requests
import os
import datetime

SERVER_URL = "http://WellE.pythonanywhere.com"
CONTROLLER_TOKEN = '1234567890'
SMS_MESSAGE_URL = "https://sms.iprogtech.com/api/v1/sms_messages"
SMS_TOKEN = "70b0567b2c219b0d124aae40865a3a38aed55355"
# params = {
#     "api_token": "70b0567b2c219b0d124aae40865a3a38aed55355",
#     "message" : "Hello, world! This is a test message",
#     "phone_number": "639466142926",
#     "sms_provider": 1
# }

SMS_TAKEN_MEDICATION_TEXT = "Hello, this is Well-E, your AI-powered medical assistant. {patient_name} has successfully taken their scheduled medication today at {schedule_time}. Medication taken: {pill}. Thank you for trusting Well-E!"
SMS_NOT_TAKEN_MEDICATION_TEXT = "Hello, this is Well-E, your AI-powered medical assistant. {patient_name} has not taken their scheduled medication today at {schedule_time}. Thank you for trusting Well-E!"


def send_message(message : str , phone_number : str):
    if not message or not phone_number:
        return
    params = {
        "api_token": SMS_TOKEN,
        "message" : message,
        "phone_number": phone_number,
        "sms_provider": 1
    }
    try:
        
        response = requests.post(url=SMS_MESSAGE_URL, params=params)
        if response.ok:
            return response.json()
        else:
            print(f'Server responded with status: {response.status_code}')
            print(f'Error: {response.json()}')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None



def send_post_request():
    try:
        url = SERVER_URL + '/controller'  # Replace with your actual URL
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            'controller_token': CONTROLLER_TOKEN  # Replace with your actual token
        }
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.ok:
            return response.json()
        else:
            print(f'Server responded with status: {response.status_code}')
            print(f'Error: {response.json()}')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None

def delete_schedule(schedule_id):
    try:
        url = SERVER_URL + '/controller/delete'  # Replace with your actual URL
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            'controller_token': CONTROLLER_TOKEN,  # Replace with your actual token
            'schedule_id' : schedule_id
        }
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.ok:
            return response.json()
        else:
            print(f'Server responded with status: {response.status_code}')
            print(f'Error: {response.json()}')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None

def taken_medicine_schedule(schedule_id): 
    try:
        url = SERVER_URL + '/controller/taken'  # Replace with your actual URL
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            'controller_token': CONTROLLER_TOKEN,  # Replace with your actual token
            'schedule_id' : schedule_id
        }
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.ok:
            return response.json()
        else:
            print(f'Server responded with status: {response.status_code}')
            print(f'Error: {response.json()}')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None





def fetch_and_save_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        
        if response.status_code == 200:
            if not os.path.isfile(save_path):
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"Image saved to {save_path}")
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error: {e}')

# Example usage
# image_url = 'http://example.com/image.jpg'  # Replace with your actual image URL
# save_path = 'path/to/save/image.jpg'  # Replace with your desired save path
# fetch_and_save_image(image_url, save_path)


def extract_filename(url):
    pattern = r'/([^/]+)$'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# Example usage
# url = 'http://example.com/media/nurse_faces/nurse_image.jpg'
# filename = extract_filename(url)
# print(filename)  # Output: nurse_image.jpg


def text_to_dictionary(response: str):
    if not isinstance(response, str):
        print("Response must be a string")
        return None

    try:
        # Use a regex pattern to extract the full JSON content
        match = re.search(r'\{[\s\S]*\}', response)
        if match:
            # Extract the matched JSON-like text
            json_text = match.group(0)

            # Parse the JSON
            return json.loads(json_text)
        else:
            print("No JSON-like content found in the response")
            return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

        

def text_to_list(text):
    # Find the list within the text
    match = re.search(r'\[.*?\]', text)
    if match:
        # Extract the list text
        list_text = match.group(0)
        
        # Convert the list text to a Python list
        try:
            return json.loads(list_text)
        except json.JSONDecodeError:
            print("Failed to parse JSON from the list")
            return None
    else:
        print("No list found in the text")
        return None

# Example usage
# text = "List ['{\"name\": \"John\"}', 'Hello', '{\"age\": 30}']"
# result = extract_and_convert_list(text)
# print(result)  # Output: ['{"name": "John"}', 'Hello', '{"age": 30}']
 

def extract_integer(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group(0))
    else:
        return None

# Example usage
# text = "patient-1"
# integer = extract_integer(text)
# print(integer)  # Output: 1


def extract_integer_and_text(text):
    match = re.search(r'(\D+)-(\d+)', text)
    if match:
        text_part = match.group(1)
        integer_part = int(match.group(2))
        return text_part, integer_part
    else:
        return None, None

# Example usage
# text = "patient-1"
# text_part, integer_part = extract_integer_and_text(text)
# print(f"Text: {text_part}, Integer: {integer_part}")  # Output: Text: patient, Integer: 1
 
def convert_str_to_date(str_to_date):
    if str_to_date:
        return datetime.datetime.strptime(str_to_date, "%Y-%m-%d %H:%M")
    else:
        return None

def convert_str_to_time(str_to_time):
    if str_to_time:
        return datetime.datetime.strptime(str_to_time, "%H:%M")
    else:
        return None
    
  
def is_within_time_range(start_time_str, offset_minutes):
    # Get the current date and time
    now = datetime.datetime.now()
    
    # Parse the start time
    start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
    
    # Combine the start time with today's date
    start_datetime = datetime.datetime.combine(now.date(), start_time)
    
    # Calculate the end time by adding the offset minutes
    end_datetime = start_datetime + datetime.timedelta(minutes=offset_minutes)
    
    # Check if the current time is within the range
    return start_datetime <= now <= end_datetime

# Example usage
# start_time_str = "23:42"  # 1:00 AM in 24-hour format
# offset_minutes = 30

# if is_within_time_range(start_time_str, offset_minutes):
#     print("Current time is within the specified time range.")
# else:
#     print("Current time is outside the specified time range.")



def is_current_date(date_str):
    # Get the current date
    today = datetime.date.today()
    
    # Parse the date string
    input_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    
    # Check if the input date is the current date
    return input_date == today

# Example usage
# date_str = "2025-01-27"

# if is_current_date(date_str):
#     print("The provided date is the current date.")
# else:
#     print("The provided date is not the current date.")




def check_date_status(date_str):
    # Parse the input date string into a datetime object
    input_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    
    # Get the current date
    current_date = datetime.datetime.now().date()
    
    # Compare the dates
    if input_date < current_date:
        return "Past"
    elif input_date == current_date:
        return "Present"
    else:
        return "Future"

 
def check_time_status(time_str, minutes):
    # Parse the input time string into a datetime object (time today)
    now = datetime.datetime.now()
    input_time = datetime.datetime.strptime(time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
    
    # Create a time range: current_time ± minutes
    time_window_start = now - datetime.timedelta(minutes=minutes)
    time_window_end = now + datetime.timedelta(minutes=minutes)
    
    # Check if the input time is within the time window
    if time_window_start <= input_time <= time_window_end:
        return "Present"
    elif input_time < now:
        return "Past"
    else:
        return "Future"


# Example usage
# time_to_check = "17:27"
# minutes_window = 30  # 30 minutes
# status = check_time_status(time_to_check, minutes_window)
# print(f"The time {time_to_check} is in the {status}.")
