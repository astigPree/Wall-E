
import json
import threading
import time
from copy import deepcopy

class DataHandler(threading.Thread):
    
    authorized_user = False # True if authorized user 
    """
        User must say the password first to do the action to be authorized to use the assistant
    """
    stop_the_loop = False # Use to stop the loop of the thread
    
    
    items_filename = "items.json"
    users_filename = "users.json"
    schedule_filename = "schedules.json"
    

    items : dict = None
    """
     {
         "item_id": {
             "item": "Item Name",
             "place": "Item Location"
         },
         #...
     }
    """
    
    user : dict = None
    """
     {
        "master": "Makie Tech",
        "assistant": "Odilon",
        "password": "makietech"
     }
    """
    
    schedules : dict = None
    """
    {
        "schedule_id": {
            "schedule": "2023-05-10 12:00:00",
            "activity": "read a book"
        },
        #...
    }
    """
    
    
    
    
    has_changes_in_items = False # Use to track if there is any changes in the items
    has_changes_in_users = False # Use to track if there is any changes in users
    has_changes_in_schedules = False # Use to track if there is any changes in schedules
    
    
    def __init__(self):
        self.load_items()
        self.load_users()
        self.load_schedules()

    
    # ========================== READ ==========================
    def load_items(self):
        with open(self.items_filename, "r") as file:
            self.items = json.load(file)
    
    def load_users(self):
        with open(self.users_filename, "r") as file:
            self.user = json.load(file)
    
    def load_schedules(self):
        with open(self.schedule_filename, "r") as file:
            self.schedules = json.load(file)
    
    def get_item(self, item_id : int):
        return self.items[item_id]

    def get_schedule(self, schedule_id : int):
        return self.schedules[schedule_id]

    def get_items(self):
        return self.items

    def get_schedules(self):
        return self.schedules

    def get_user(self):
        return self.user

    def get_master(self):
        return self.user["master"]

    def get_assistant(self):
        return self.user["assistant"]

    def get_password(self):
        return self.user["password"]

    def get_schedule_by_date(self, date : str):
        schedules = []
        for schedule_id, schedule in self.schedules.items():
            if schedule["schedule"].startswith(date):
                schedules.append(schedule)
        return schedules

    def get_schedule_by_activity(self, activity : str):
        schedules = []
        for schedule_id, schedule in self.schedules.items():
            if schedule["activity"] == activity:
                schedules.append(schedule)
        return schedules


    # ========================== WRITE ==========================
    def save_items(self):
        items = deepcopy(self.items)
        with open(self.items_filename, "w") as file:
            json.dump(items, file)
    
    def save_users(self):
        user = deepcopy(self.user)
        with open(self.users_filename, "w") as file:
            json.dump(user, file)
    
    def save_schedules(self):
        schedules = deepcopy(self.schedules)
        with open(self.schedule_filename, "w") as file:
            json.dump(schedules, file)

    def add_item(self, name : str, place : str):
        item_id = list(self.items.keys())[-1]
        self.items[item_id] = {
            "item": name,
            "place": place
        }
    
    def remove_item(self, item_id : int):
        if item_id in self.items:
            del self.items[item_id]
    
    def update_item(self, name : str, place : str, item_id : int):
        self.items[item_id] = {
            "item": name,
            "place": place
        }

    def add_schedule(self, schedule : str, activity : str):
        schedule_id = list(self.schedules.keys())[-1]
        self.schedules[schedule_id] = {
            "schedule": schedule,
            "activity": activity
        }
        
    def remove_schedule(self, schedule_id : int):
        if schedule_id in self.schedules:
            del self.schedules[schedule_id]

    def update_schedule(self, schedule : str, activity : str, schedule_id : int):
        self.schedules[schedule_id] = {
            "schedule": schedule,
            "activity": activity
        }

    
    
    
    # Thread Running
    def run(self):
        frame = 1 / 30
        while not self.stop_the_loop:
            
            
            
            if self.has_changes_in_items:
                self.save_items()
                self.has_changes_in_items = False
            if self.has_changes_in_users:
                self.save_users()
                self.has_changes_in_users = False
            if self.has_changes_in_schedules:
                self.save_schedules()
                self.has_changes_in_schedules = False

            
            
            time.sleep(frame) # Sleep for 30 second per frame to avoid busy loop





class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print(f"Starting thread: {self.name}")
        self.print_time(self.name, self.counter, 5)
        print(f"Exiting thread: {self.name}")

    def print_time(self, thread_name, delay, counter):
        while counter:
            time.sleep(delay)
            print(f"{thread_name}: {time.ctime(time.time())}")
            counter -= 1



# Create new threads
thread1 = MyThread(1, "Thread-1", 1)
thread2 = MyThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

# Wait for all threads to complete
thread1.join()
thread2.join()

print("Exiting Main Thread")
