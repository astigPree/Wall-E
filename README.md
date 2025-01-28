# Pill Dispenser Machine

## Client Requirements
- **Pill Dispenser:** To dispense the medication.
- **Locking System:** To secure the medication compartment.
- **Light Indicator:** To show if the medication is running low or if there is an issue.
- **Body Temperature:** To monitor the user's body temperature.
- **Medication Schedule Display:** To show the medication schedule on an LED.
- **Medication Reminder:** To remind users of their medication times.
- **Facial Recognition:** To identify authorized users for loading and taking medication.
- **Fall Detection (Suggested):** To detect if the machine has fallen.

## Not Considered
- **Movement of the Machine**

## Solution

1. **Pill Dispenser**
    - Utilizes a stepper motor (28BYJ-48 Stepper Motor) and driver (ULN2003) to dispense pills by rotating a wheel.
    - [Reference Video](https://www.youtube.com/watch?v=JeFL72bqpLk)

2. **Locking System**
    - Uses a servo motor (Tower Pro SG90) to lock the back of the machine.
    - Controlled by a microcontroller and Bluetooth module.
    - [Reference Video](https://www.youtube.com/watch?v=44yhoZ69Q78)

3. **Light Indicator**
    - Uses an RGB LED module to indicate medication status or health alerts.
    - Controlled by a microcontroller and Bluetooth module.

4. **Body Temperature**
    - Uses MAX30205 sensor to detect and display body temperature on an OLED LCD or through voice output.
    - [Reference Video](https://www.youtube.com/watch?v=h9hUZQc4oLE&t=57s)

5. **Medication Schedule Display**
    - Uses an RGB LED module to show medication schedules.
    - Controlled by a microcontroller and Bluetooth module.

6. **Medication Reminder**
    - Uses an RGB LED module and a speaker to notify users of medication times.

7. **Facial Recognition**
    - Uses a camera module on a Raspberry Pi 3B to capture and compare user faces with a database.
    - Identifies users for accessing medication (Nurses) or taking medication (Patients).

8. **Fall Detection (Suggested)**
    - Uses an IR sensor module to detect if an object has dropped into the pill box.
