from my_tools import *
import time

while True:
    data = send_post_request()
    if data:
        print(f"Received data: {data}")
    time.sleep(3)