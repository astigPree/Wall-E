from my_tools import *
import time
 
data = send_post_request()
if data:
    print(f"Received data: {data}")

import datetime

def is_current_date(date_str):
    # Get the current date
    today = datetime.date.today()
    
    # Parse the date string
    input_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    
    # Check if the input date is the current date
    return input_date == today

# Example usage
date_str = "2025-01-27"

if is_current_date(date_str):
    print("The provided date is the current date.")
else:
    print("The provided date is not the current date.")
