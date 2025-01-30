#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <MFRC522.h>
#include <avr/pgmspace.h>

#define RST_PIN 9
#define SS_PIN 10

LiquidCrystal_I2C lcd(0x27, 16, 2);
MFRC522 mfrc522(SS_PIN, RST_PIN);

// Store checked-in UIDs
String checkedInUIDs[50];  // Stores scanned UIDs (max 50, increase if needed)
int checkedCount = 0;      // Tracks number of checked-in users

// Function to retrieve name from RFID UID
String getNameFromUID(String uid) {
    if (uid == "44 A2 37 F9") return "Fritz Andrei Povadora Gepiga";
  else if (uid == F("44 59 2E F9")) return F("Virgil Jr. Berezo");
  else if (uid == F("C4 6B 2B DB")) return F("Charles Darwyne Alcos");
  else if (uid == F("C4 94 22 DB")) return F("Jorros Daniel Coca");
  else if (uid == F("64 BD 28 F9")) return F("Arween Louise Justalero");
  else if (uid == F("D4 DE 26 F9")) return F("Aiza Ancajas Nulla");
  else if (uid == F("A4 D6 7B DF")) return F("Krist Ian Loie Roa");
  else if (uid == F("C4 B4 85 DF")) return F("Sophia Aices Sullano ");
  else if (uid == F("14 EB 19 DB")) return F("Charade Anne Grado");
  else if (uid == F("C4 69 29 F9")) return F("Carmela Jane Mata");
  else if (uid == F("44 CB 86 DF")) return F("Paul Joshua Dy");
  else if (uid == F("B4 75 81 DF")) return F("John Aica Cabañero");
  else if (uid == F("74 8C 2A DB")) return F("Andre Evanz Etulle");
  else if (uid == F("14 AF 75 DF")) return F("Jenny Villarosa Veral");
  else if (uid == F("D4 B8 59 DF")) return F("Mercy Joy Ytang Mabida");
  else if (uid == F("E4 8D 5D DF")) return F("John Rexy Bato-on");
  else if (uid == F("C4 D0 85 DF")) return F("Mera Yhen Abayon");
  else if (uid == F("4 6F 89 DF")) return F("Karylle Templado");
  else if (uid == F("C4 94 22 DB")) return F("Ralph Josef Baruman");
  else if (uid == F("A4 C3 70 DF")) return F("Cathyrine Genita");
  else if (uid == F("34 3F 29 F9")) return F("Shannel Marie Sividan");
  else if (uid == F("34 E7 3B DB")) return F("KC Caballes Padernal");
  else if (uid == F("94 6E 2A DB")) return F("Ryz Gomez");
  else if (uid == F("84 57 78 DF")) return F("Ma Venezia Carmel Albacite");
  else if (uid == F("54 AB 59 DF")) return F("Ivan Jay Selle Ranili");
  else if (uid == F("74 92 2E F9")) return F("Alexia Jedah Jayme");
  else if (uid == F("C4 B6 1E DB")) return F("Louie Jay Roxas");
  else if (uid == F("A4 AB 26 F9")) return F("Joshua Arangote");
  else if (uid == F("74 17 84 DF")) return F("Stephanie Ambay");
  else if (uid == F("24 D3 32 F9")) return F("Kim Rose Dela Torre");
  else if (uid == F("B4 14 40 DB")) return F("Zj M. Alicaya");
  else if (uid == F("74 99 28 F9")) return F("Charmelle Adolfo");
  else if (uid == F("A4 A1 2D F9")) return F("Asterio Delfin Montebon Jr.");
  else if (uid == F("44 B5 1A DB")) return F("Princess Ronamie Magnetico");
  else if (uid == F("4 43 55 DF")) return F("John Earl Aying Dotosme");
  else if (uid == F("24 0F 51 DF")) return F("Alreese Niña Mabalay");
  else if (uid == F("14 3D 7C DF")) return F("Natalie Marie Bas Quitos");
  else if (uid == F("A4 36 20 DB")) return F("Brylle Dominique Villagracia");
  else if (uid == F("B4 1F 77 DF")) return F("Nickie Manayaga Aguirre");
  else if (uid == F("44 BA 31 F9")) return F("Paolo Miguel G. Bahala");
  else if (uid == F("94 D7 7D DF")) return F("Jona Mae Miñoza");
  else if (uid == F("14 FE 32 F9")) return F("Tristan Bilonoac");
  else if (uid == F("84 70 27 F9")) return F("Blaise Orphen John Cortez");
  else if (uid == F("C4 18 30 F9")) return F("Alyza Therina Congson Irag");
  else if (uid == F("C4 B7 2F DB")) return F("Nathaniel Inocando P.");
    else return "Unknown"; // Default case if UID is not recognized
}

// Function to check if the user has already scanned
bool isAlreadyCheckedIn(String uid) {
    for (int i = 0; i < checkedCount; i++) {
        if (checkedInUIDs[i] == uid) {
            return true; // Found in the checked-in list
        }
    }
    return false;
}

// Function to register UID as checked-in
void markCheckedIn(String uid) {
    if (checkedCount < 50) {  // Prevent overflow
        checkedInUIDs[checkedCount++] = uid;
    }
}

void setup() {
    Serial.begin(9600);
    SPI.begin();
    mfrc522.PCD_Init();
  
    lcd.init();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("Scan Your Card");
    Serial.println("Ready to scan RFID tag...");
}

void loop() {
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        return;
    }

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Reading...");

    // Get UID from scanned card
    String uid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        uid += String(mfrc522.uid.uidByte[i], HEX);
        if (i < mfrc522.uid.size - 1) {
            uid += " ";
        }
    }
    uid.toUpperCase();
    Serial.print("RFID Tag UID: ");
    Serial.println(uid);

    String name = getNameFromUID(uid);
  
    lcd.clear();
    lcd.setCursor(0, 0);

    if (name == "Unknown") {
        lcd.print("UNKNOWN USER");
        lcd.setCursor(0, 1);
        lcd.print("NOT RECORDED!");
        Serial.println("Unknown User - Attendance Not Recorded!");
    } else {
        if (isAlreadyCheckedIn(uid)) {
            lcd.print("ALREADY CHECKED!");
            Serial.println("Attendance Already Checked for: " + name);
        } else {
            lcd.print("ATTENDANCE VERIFIED!");
            lcd.setCursor(0, 1);
            lcd.print(name);
            Serial.println("Attendance Verified for: " + name);
            markCheckedIn(uid); // Save UID as checked-in
        }
    }

    mfrc522.PICC_HaltA();
    delay(3000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Scan Your Card");
}
