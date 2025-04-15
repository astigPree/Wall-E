
------------------------------------------------------------------------------------------------------------------------
Here’s the complete guide to connect your Raspberry Pi to a Windows PC using a LAN cable and access it via the LAN port:

---

### **Explanation of the Setup**

When you connect your Raspberry Pi to a Windows PC using an Ethernet cable directly to the LAN port:
- Both devices must be on the same subnet for communication.
- A static IP address must be assigned to both the Raspberry Pi and the Windows PC since there's no DHCP server to assign addresses automatically.
- This connection creates a private network between your Raspberry Pi and the Windows PC, allowing services like SSH, file sharing, and web hosting to be accessed using the Raspberry Pi's IP address.

---

### **Step-by-Step Instructions**

#### **1. Prepare the Raspberry Pi (Already Completed)**
- Ensure your Raspberry Pi is configured with a static IP address, e.g., `192.168.1.20`.
- Make sure SSH is enabled using `sudo raspi-config` and that any required services (like Samba for file sharing) are properly set up.

#### **2. Connect Raspberry Pi to Windows PC**
- Use a standard Ethernet cable to connect the LAN port of your Raspberry Pi to the LAN port of your Windows PC.

---

#### **3. Set Up the Windows PC**
1. **Assign a Static IP Address**:
   - Open the **Network and Sharing Center**:
     - Press `Windows + R`, type `ncpa.cpl`, and press Enter.
   - Right-click your **Ethernet** connection and select **Properties**.
   - Select **Internet Protocol Version 4 (TCP/IPv4)** and click **Properties**.
   - Configure the following settings:
     - **IP Address**: `192.168.1.1` (you can choose another address as long as it’s on the same subnet, e.g., `192.168.1.x`).
     - **Subnet Mask**: `255.255.255.0`.
     - **Default Gateway**: Leave this blank.
   - Click **OK** to save.

2. **Test the Connection**:
   - Open Command Prompt (`Windows + R`, type `cmd`, and press Enter).
   - Ping the Raspberry Pi's IP address to check connectivity:
     ```bash
     ping 192.168.1.20
     ```
   - If you see replies, the connection is working.

---

#### **4. Access the Raspberry Pi**
You can now access your Raspberry Pi using the following methods:

**a. Access via SSH**:
- Open Command Prompt or install **PuTTY** on your Windows PC.
- Use the following command to connect via SSH:
  ```bash
  ssh pi@192.168.1.20
  ```
- Enter your Raspberry Pi’s password when prompted.

**b. File Sharing**:
- If Samba is set up on your Raspberry Pi:
  - Open File Explorer on your Windows PC.
  - In the address bar, type:
    ```bash
    \\192.168.1.20
    ```
  - Log in using your Raspberry Pi credentials to access shared folders.

**c. Web Server Access (Optional)**:
- If your Raspberry Pi is running a web server:
  - Open your browser and go to:
    ```bash
    http://192.168.1.20
    ```

---

#### **5. Firewall Configuration (If Needed)**
- Ensure the Windows Firewall allows the required services, such as SSH and Samba.
   - Go to **Control Panel > System and Security > Windows Defender Firewall > Allow an app through the firewall**.
   - Enable access for SSH (port 22), Samba, or any other services running on the Raspberry Pi.

---

Following these steps, your Windows PC should successfully connect to your Raspberry Pi through the LAN cable, allowing seamless communication and access via its static IP (`192.168.1.20`). Let me know if any part of the setup needs clarification!


------------------------------------------------------------------------------------------------------------------------

Certainly! Here's the updated, complete guide for connecting and setting up your Arduino Mega:

---

### **Arduino Mega Pinout Guide**

#### **1. Servo Motors for Pill Dispensers**
- **Biogesic Servo:** Connect the signal pin to Pin **4**.
- **Cremils Servo:** Connect the signal pin to Pin **5**.
- **Citirizene Servo:** Connect the signal pin to Pin **7**.
- **Mefenamic Servo:** Connect the signal pin to Pin **6**.

#### **2. Pills Detector (IR Sensor)**
- **IR Sensor:** Connect the signal pin to Pin **40**.

#### **3. Lock Servo Motor**
- **Lock Servo:** Connect the signal pin to Pin **13**.

#### **4. RFID Module**
- **SDA (Serial Data):** Connect to Pin **9** on the Arduino Mega.
- **RST (Reset):** Connect to Pin **8** on the Arduino Mega.
- **MOSI (Master-Out Slave-In):** Connect to Pin **51** on the Arduino Mega.
- **MISO (Master-In Slave-Out):** Connect to Pin **50** on the Arduino Mega.
- **SCK (Clock):** Connect to Pin **52** on the Arduino Mega.
- **GND (Ground):** Connect to any GND pin on the Arduino Mega.
- **3.3V or 5V Power:** Connect to the 3.3V or 5V pin (depending on the RFID module's requirements).

#### **5. Color Sensors**
- **Left Sensor:**
  - **S0:** Connect to Pin **24**.
  - **S1:** Connect to Pin **25**.
  - **S2:** Connect to Pin **26**.
  - **S3:** Connect to Pin **27**.
  - **Sensor Out:** Connect to Pin **28**.

- **Right Sensor:**
  - **S0:** Connect to Pin **29**.
  - **S1:** Connect to Pin **30**.
  - **S2:** Connect to Pin **31**.
  - **S3:** Connect to Pin **32**.
  - **Sensor Out:** Connect to Pin **33**.

#### **6. Motor Drivers for Wheels**
- **Right Wheel:**
  - **Motor Pin:** Connect to Pin **36**.
  - **Direction Pin:** Connect to Pin **37**.

- **Left Wheel:**
  - **Motor Pin:** Connect to Pin **38**.
  - **Direction Pin:** Connect to Pin **39**.

#### **7. Temperature Sensor (MLX90614)**
- Connect the **SDA** and **SCL** pins of the temperature sensor to the corresponding **SDA** and **SCL** pins on your Arduino Mega (Pins **20** and **21**).

---
