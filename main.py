import serial
import firebase_admin
from firebase_admin import credentials, db
import datetime

# FIREBASE CREDENTIALS NI HEREE 
cred = credentials.Certificate("firebase.json")  # Path to your JSON file
firebase_admin.initialize_app(cred, {
    "databaseURL": "" # URL of your FIREBASE
})

# lISTA SA MGA STEM STUDENT NAMES 
rfid_to_name = {
    "C4 B7 2F DB": "Nathaniel P. Inocando",

# PUT MORE LIST HERE 

}

# SET UP SA SERIAL COMMUNICATION
arduino = serial.Serial('COM6', 9600, timeout=1)  
print("Listening for RFID tags...")

# Function to check if UID is already recorded naba sa Firebase and the date today.
def is_already_checked_in_today(uid):
    attendance_ref = db.reference("attendance")
    records = attendance_ref.get()

    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

    if records:
        for record_id, record in records.items():
            if record.get("rfid") == uid:
                recorded_date = record.get("timestamp", "").split(" ")[0]
                if recorded_date == today_date:
                    return True  

    return False

while True:
    try:
        # Tig Read data sa Arduino And Tig extract UID sa data
      if arduino.in_waiting > 0:
            data = arduino.readline().decode().strip()
            print(f"Received: {data}")

            if "RFID Tag UID:" in data:
                uid = data.split(":")[1].strip()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if uid in rfid_to_name:
                    name = rfid_to_name[uid]
                    print(f"✅ Detected: {name}")

                    if is_already_checked_in_today(uid):
                        print(f"❌ Attendance already checked for {name}. Skipping Firebase record.")
                    else:
                        attendance_ref = db.reference("attendance")
                        attendance_data = {
                            "name": name,
                            "rfid": uid,
                            "timestamp": timestamp
                        }
                        attendance_ref.push(attendance_data)
                        print(f"✅ Attendance recorded for {name} at {timestamp}")

                else:
                    print("⚠️ Unknown RFID tag detected. Ignoring it.")

    except KeyboardInterrupt:
        print("\nExiting...")
        break
