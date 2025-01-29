CLIENT REQUIREMENTS;
    - pill dispenser
    - locking system
    - light indicator in ubos na med or wala pwedeng yung sa sceen ai na rin
    - body temperature
    - med schedule sa led
    - medication reminder
    - facial recognition sa user kung sino lang taga lagay ng med at sino lang taga take ng med
    - fall detection(suggest ko)

CLIENT NOT TAKEN INTO CONSIDERATION;
    - moving of the machine


SOLUTION;
    - pill dispenser
        With stepper motor (28BYJ-48 Stepper Motor) and with driver (ULN2003) the problem will be solved.
        The stepper moter will be used to dispense the pills by rotating the wheel with a certain angle to drop the pill.
        REF: https://www.youtube.com/watch?v=JeFL72bqpLk
    
    - locking system
        With the use of servo (Tower pro sg90 servo motor) it will be used to lock the back of the machine.
        It will be controlled by the microcontroller and bluetooth module.
        REF: https://www.youtube.com/watch?v=44yhoZ69Q78
    
    - light indicator in ubos na med or wala pwedeng yung sa sceen ai na rin
        With the use of RGB LED MODULE it will produce a light indicator to show the pills or any health problem notices.
        It will be controlled by the  microcontroller and bluetooth module.

    - body temperature
        With the use of MAX30205 it will be used to detect the body temperature and be display in OLED LCD or VOICE out ng machine.
        REF: https://www.youtube.com/watch?v=h9hUZQc4oLE&t=57s
    
    - med schedule sa led
        With the use of RGB LED MODULE it will produce an indicator that the schedule of the medication has been scheduled.
        It will be controlled by the  microcontroller and bluetooth module.

    - medication reminder
        With the use of RGB LED MODULE and SPEAKER it will produce an notification that the schedule of the medication has been scheduled.

    - facial recognition sa user kung sino lang taga lagay ng med at sino lang taga take ng med
        With the use of CAMERA MODULE in raspberry pi 3b it will capture the current user and compare it with the database.
        Then it will identify the user if they want to open the back of the machine (NURSEs) or take a pills (PATIENTs).
    
    - fall detection(suggest ko)
        With the use of IR SENSOR MODULE it will detect if an object dropped to the pill box.


    - moving of the machine
        With the use of stepper  motor (28BYJ-48 Stepper Motor) and with driver (ULN2003) and servo motor (Tower pro mg995).
        stepper motor will be used to move the machine to back and forward and the servo will be used to point where the machine will be moved.




SENARIOS;
    1. Power on the machine, it will on the raspberry device and arduino device.
    2. The raspberry device will start all the activities it need, example;
        - start the scripts
        - the camera will start to capture the user
    
    3. Senario in putting pills (NURSEs);
    - The user will ask the machine to open the back of the machine.
    - The machine will scan the face of the user.
    - If the user is not in the database the machine will not open the back of the machine.
    - If the user is in the database the machine will open the back of the machine.
    - The stepper motor will go back to its original position.
    - The user will put the pills in the pill slot.
    - The user will close the back of the machine.
    - The user ask the machine to close the back of the machine for security.

    4. Senario in taking pills (PATIENTs);
    - The user will ask the machine to dispense the pills;
    - The machine will scan the face of the user.
    - If the user is not in the database the machine will not dispense the pills.
    - If the user is in the database the machine will check if the user can take the pills by their schedule.
    - If the user can take the pills the machine will dispense the pills.

    5. Senario in taking pills (Machine will);
    - The machine will check the schedule of the pills.
    - If the there is a schedule the machine will speak the schedule and who will take the pills.
    - If there is no schedule the machine will not speak anything.
    - The patient must ask the machine to move or patient must move to closest place to the machine.
    - If the patient is in the closest place to the machine the machine will scan the face of the patient.
    - If the patient is not in the closest place to the machine the machine will not scan the face of the patient.
    - If the patient is in the database the machine will dispense the pills.

    6. Senario in setting schedule (NURSEs);
    - The user will ask the machine to set the schedule.
    - The machine will scan the face of the user if the user is a nurse.
    - The machine will ask for the schedule of the pills.
    - The machine will ask for the name of the patient.
    - Then the machine will ask for facial information about the patient.
    - The machine will save the schedule in the database.

    7. Senario in checking body temperature (NURSEs);
    - The user can get the body temperature of the patient by using the machine tools.
    - The machine will identify the body temperature of the patient.
    - The machine will display the body temperature of the patient and speak the body temperature of the patient.

    8. Senario in making the machine walk;
    - The user will ask the machine to move.
    - The machine will identify what position and where to go.
    - The machine will move to the position and where to go.
    
    9. Senario in making the machine talk;
    - The user will ask the machine to talk.
    - The machine will identify what to say.
    - The machine will speak what to say.

    


REQUIREMENTS;

pip install -U g4f[all]
pip install gTTS
( will be replaced ) pip install DeepFace 
pip install Pillow
( used to replaced DeepFace) pip install imagehash
pip install cv2
pip install speech_recognition
pip install playsound
( don't apply ) pip install -qq pytorch-lightning==1.7.0 transformers==4.21.3 aitextgen==0.6.0
( don't apply ) pip install torchmetrics==0.11.4
pip install pyserial 
pip install twilio



COMMAND ; 

Biogesic = "B" (raspberry)
Cremil-S = "S" (raspberry)
Citerizen = "C" (raspberry)
Mefenamic = "M" (raspberry)

Red-Patient = "RED" (raspberry)
Blue-Patient = "BLUE" (raspberry)
Yellow-Patient = "YELLOW" (raspberry)

PILL-DROPED = "DROP" (arduino)
PILL-DRINK = "DRINK" (arduino)
FINISH-LINE-COLOR = "GREEN" (arduino)
COMEBACK-COMMAND = "BACK" (raspberry)
HOME-COLOR = "PINK" (arduino)
HOME-COMMAND = "HOME" (arduino)
NO-PILLS-Biogesic = "NPB" (arduino)
NO-PILLS-Cremil-S = "NPS" (arduino)
NO-PILLS-Citerizen = "NPC" (arduino)
NO-PILLS-Mefenamic = "NPM" (arduino)

SENARIOS ARDUINO;

Walking;
    - (raspberry) masend ako san command kun sa diin na color na makadto
        - Masiyak na may importante na karadtuon
    - (arduino) masend san command na nakaabot na an machine sa FINISH-LINE-COLOR
        - detect pag may nakaharang
    - (raspberry) Masiyak san patient name tapos suguon na mag kita sa machine camera
    - (raspberry) Pag wara mag pakita sa machine camera in specific time then masend san command na mag uli na
        - (arduino) Matalikod tas mabalik sa pinangalingan
        - (raspberry) Masiyak na mauli na sya
        - (arduino) Masend san command na nakauli na sya
            - detect pag may nakaharang
    - (raspberry) Pag may nakita na patient sa camera identify ko an pamayhon kun hahatagan san bulong
        - (raspberry) Masend san signal san bulong na kailangan san patiente
            - maistorya na maghulat sa pag takdag san bulong
        - (arduino) matagdak san bulong at mapailaw
            - (arduino) masend san command na natakdag na PILL-DROPED
            - (raspberry) masiyak na kuhaon na an bulong tas after 5 mins
            - (raspberry) after 5 mins tas wara pa san command na nakaabot galing sa arduino, mauli na an robot
            - (arduino) pag may action na tinumar tas nag pindot sa arduino, masend san command na PILL-DRINK
            - (raspberry) mahulat san 1 minute bago mag uli para makapag storya lang sa patiente san kadali
            - (raspberry) masend san commandna maguli na COMEBACK-COMMAND
            - (arduino) masend san command na nakauli na sya 
                - detect pag may nakaharang
        - (arduino) pagwara san bulong, masend san command
            - (arduino) masend san command na waran bulong NO-PILLS
            - (raspberry) masiayak na wara na akon bulong sani na pills
            - (raspberry) masiayak na mauli sya para mag sabi na wara na sya san bulong 
            - (arduino) masend san command na nakauli na sya 
                - detect pag may nakaharang
            - (raspberry) masiyak na need nya san bulong for 1 mins pag kauli

        REPEATE THE CYCLE IF NECCESSARY 



Body Temperature;

    - (raspberry) masend san command na madetect san body temperature san tawo tas mahulat san 2 minutes
    - (arduino) madect san temperature san tawo hasta may command na mag abot
    - (raspberry) pag tapos na an minutes masend san command sa arduino na tapos na 
    - (raspberry) maistorya san average temperature


