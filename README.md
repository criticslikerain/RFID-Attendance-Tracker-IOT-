RFID Attendance Tracker with IoT and Firebase Integration
=========================================================

A real-time attendance tracking system using RFID, Arduino, and Firebase to manage attendance efficiently. The system integrates a Python backend for database operations and an I2C LCD for user feedback.

---------------------------------------------------------
Features:
---------
- Real-time attendance logging to Firebase.
- Ensures no duplicate attendance records for the same day.
- User feedback through an I2C LCD display.
- Python backend for UID validation and Firebase communication.

---------------------------------------------------------
Project Structure:
------------------
RFID-Attendance-Tracker/
├── CONTROLLER/
│   ├── CONTROLLER.ino          # Arduino code for RFID and LCD handling
│   ├── I2C_Address_Finder.ino  # Arduino code to find the LCD I2C address
├── data/
│   ├── arduino.PNG             # Arduino wiring diagram
│   ├── RFID connections.PNG    # RFID wiring details
│   ├── Specifications.PNG      # Project specifications
├── firebase.json               # Firebase Admin SDK config file
├── main.py                     # Python backend script
└── README.txt                  # Project README file

---------------------------------------------------------
Getting Started:
----------------
1. Hardware Requirements:
   - Arduino Uno/Nano/Mega
   - RFID Module (RC522)
   - I2C LCD Display (16x2)
   - Breadboard and Jumper Wires

2. Software Requirements:
   - Arduino IDE
   - Python (3.x)
   - Firebase Project

---------------------------------------------------------
Setup Instructions:
-------------------
1. Arduino Setup:
   - Open the `CONTROLLER.ino` file in the Arduino IDE.
   - Install the required libraries in Arduino IDE:
     - MFRC522
     - LiquidCrystal_I2C
   - Upload the code to the Arduino board.
   - Ensure the LCD displays "Scan Your Card" on startup.

2. Firebase Setup:
   - Create a Firebase project at https://console.firebase.google.com/.
   - Enable Realtime Database and set rules for read/write access.
   - Download the Firebase Admin SDK JSON file, rename it to `firebase.json`, and place it in the project folder.

3. Python Backend:
   - Install Python libraries:
     pip install pyserial firebase-admin
   - Run the Python script:
     python main.py

---------------------------------------------------------
How It Works:
-------------
1. Power on the Arduino system. The LCD displays "Scan Your Card".
2. Scan an RFID tag. The UID is sent to the Python backend.
3. The backend checks Firebase for duplicate entries. If not found, it logs the UID.
4. Attendance data can be viewed in Firebase Realtime Database.

---------------------------------------------------------
Hardware Connections:
---------------------
RFID Module:
  - SDA -> Pin 10
  - SCK -> Pin 13
  - MOSI -> Pin 11
  - MISO -> Pin 12
  - GND -> GND
  - RST -> Pin 9
  - 3.3V -> 3.3V

I2C LCD Display:
  - GND -> GND
  - VCC -> 5V
  - SDA -> A4
  - SCL -> A5

---------------------------------------------------------
Troubleshooting:
----------------
- No Text on LCD:
  - Run the `I2C_Address_Finder.ino` sketch to determine the LCD's I2C address.
  - Update the address in the `CONTROLLER.ino` file.

- RFID Not Detected:
  - Verify module connections.
  - Ensure the `MFRC522` library is installed in Arduino IDE.

- Firebase Errors:
  - Ensure the `firebase.json` file contains correct credentials.
  - Verify that Firebase rules allow read/write access.

---------------------------------------------------------
License:
--------
This project is licensed under the MIT License. You are free to use, modify, and distribute this project as needed.

---------------------------------------------------------
Contact:
--------
For inquiries or assistance, feel free to reach out!

