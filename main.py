import serial
import firebase_admin
from firebase_admin import credentials, db
import datetime

# FIREBASE CREDENTIALS NI HEREE 
cred = credentials.Certificate("rfid-attendance-a69e4-firebase-adminsdk-fbsvc-3e948be124.json")  # Path to your JSON file
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://rfid-attendance-a69e4-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# lISTA SA MGA STEM STUDENT NAMES 
rfid_to_name = {
    "44 A2 37 F9": "Fritz Andrei Povadora Gepiga",
    "44 59 2E F9": "Virgil Jr. Saga Berezo",
    "C4 6B 2B DB": "Charles Darwyne Cuanan Alcos",
    "C4 94 22 DB": "Jorros Daniel Coca",
    "64 BD 28 F9": "Arween Louise Señerpida Justalero",
    "D4 DE 26 F9": "Aiza Ancajas Nulla",
    "A4 D6 7B DF": "Krist Ian Loie Sinining Roa",
    "C4 B4 85 DF": "Sophia Aices Sullano Orcia",
    "14 EB 19 DB": "Charade Anne Amarillo Grado",
    "C4 69 29 F9": "Carmela Jane Gerebese Mata",
    "44 CB 86 DF": "Paul Joshua Alojado Dy",
    "B4 75 81 DF": "John Aica Cabañero Armentano",  
    "74 8C 2A DB": "Andre Evanz Etulle Carin",
    "14 AF 75 DF": "Jenny Villarosa Veral",
    "D4 B8 59 DF": "Mercy Joy Ytang Mabida",
    "E4 8D 5D DF": "John Rexy Palomares Bato-on",
    "C4 D0 85 DFF": "Mera Yhen Cristobal Abayon",
    "4 6F 89 DF": "Karylle Templado Castellano",
    "C4 94 22 DB": "Ralph Josef Baruman Rosca",
    "A4 C3 70 DF": "Cathyrine Genita Jizmundo",
    "34 3F 29 F9": "Shannel Marie Sividan Cañete",
    "34 E7 3B DB": "KC Caballes Padernal",
    "94 6E 2A DB": "Ryz Gomez Bulingbuling",
    "84 57 78 DF": "Ma Venezia Carmel Albacite Carpitanos",
    "54 AB 59 DF": "Ivan Jay Selle Ranili",
    "74 92 2E F9": "Alexia Jedah Jayme Rosell",
    "C4 B6 1E DB": "Louie Jay Roxas Berdon",
    "A4 AB 26 F9": "Joshua Arangote",
    "74 17 84 DF": "Stephanie Ambay Barcial",
    "24 D3 32 F9": "Kim Rose Dela Torre Medida",
    "B4 14 40 DB": "Zj M. Alicaya",
    "74 99 28 F9": "Charmelle Adolfo",
    "A4 A1 2D F9": "Asterio Delfin Montebon Jr.",
    "44 B5 1A DB": "Princess Ronamie Magnetico Otarra",
    "4 43 55 DF": "John Earl Aying Dotosme",
    "24 F 51 DF": "Alreese Niña Mabalay Labay",
    "14 3D 7C DF": "Natalie Marie Bas Quitos",
    "A4 36 20 DB": "Brylle Dominique Villagracia Salo",
    "B4 1F 77 DF": "Nickie Manayaga Aguirre",
    "44 BA 31 F9": "Paolo Miguel G. Bahala",
    "94 D7 7D DF": "Jona Mae Miñoza Pepito",
    "14 FE 32 F9": "Tristan Bilonoac Cabiging",
    "84 70 27 F9": "Blaise Orphen John Cortez",
    "C4 18 30 F9": "Alyza Therina Congson Irag",
    "C4 B7 2F DB": "Nathaniel P. Inocando"
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
