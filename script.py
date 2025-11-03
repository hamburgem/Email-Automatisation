import smtplib
import csv
import os
import getpass
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Credentials input
EMAIL_ADDRESS = input("📧 Enter your Gmail address: ")
EMAIL_PASSWORD = getpass.getpass("🔐 Enter your 16-digit App Password: ")

# Test login first
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("✅ Login successful!\n")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit()

# PDF to attach
PDF_PATH = "Lebenslauf.pdf"
if not os.path.exists(PDF_PATH):
    print(f"❌ PDF file not found: {PDF_PATH}")
    exit()

# Open CSV
with open('contacts.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        print("Current row:", row)
        name = row.get('Name').strip()
        email = row.get('Email').strip()
        unternehmen= row.get('Unternehmen')
        geschlecht = row.get('Geschlecht')

        if not name or not email:
            print("⚠️ Skipping row with missing data:", row)
            continue

        print(f"📤 Preparing to send to: {name} ({email})")

        if geschlecht==0:
            NAME= f"geehrte Frau {name}"
        elif geschlecht==1:
            NAME= f"geehrter Herr {name}"
        else:
            NAME= f"geehrtes Team der {unternehmen}"

        # Email body
        body = f"""Sehr {NAME},

ich hoffe, diese Nachricht erreicht Sie wohlbehalten.

Mit großem Interesse habe ich Ihre Anzeige für den Ausbildungsplatz als Fachinformatiker für Anwendungsentwicklung gelesen. Gerne bewerbe ich mich hiermit auf diese Stelle.

Kurz zu mir: Ich studiere derzeit im dritten Jahr Informatik an einer Universität in Marokko. Ich habe praktische Kenntnisse in C/C++, Python(Pandas, NumPy, Matplotlib, Sklearn), MySQL, HTML/CSS/JavaScript(jQuery, React, Node.js) sowie in Computernetzwerke und arbeite gerne praxisorientiert an IT-Lösungen. Meine Deutschkenntnisse liegen auf B2-Niveau und ich bin sehr motiviert, die Ausbildung in Deutschland zu beginnen.

Meinen Lebenslauf finden Sie im Anhang.


Ich hätte noch ein paar Fragen und würde mich über eine kurze Rückmeldung freuen:

- Ist eine Bewerbung aus dem Ausland (Marokko) möglich und geben Sie ausländischen Bewerbern eine Chance auf einen Ausbildungsplatz?
- Reicht ein Nachweis von Deutsch B2 aus, oder fordern Sie höhere Sprachkenntnisse/Zertifikate?
- Welche Bewerbungsunterlagen benötigen Sie in meinem Fall (zusätzliche Zeugnisse, Zeugnisanerkennung, Sprachzertifikat o.ä.)?
- Gibt es ein Online-Bewerbungsportal oder genügt diese E-Mail als Erstkontakt?
- Besteht die Möglichkeit für ein kurzes persönliches oder digitales Gespräch (Telefon/Video), um Erwartungen und Ablauf zu klären? Ich bin werktags in der Regel ab 10:00 Uhr (UTC+2) verfügbar — nennen Sie mir gern einen für Sie passenden Termin.

Ich freue mich auf Ihre positive Rückmeldung und stehe Ihnen für Rückfragen oder zum Zusenden weiterer Unterlagen jederzeit zur Verfügung.

Mit freundlichen Grüßen
Yassin Bouih
Email: yassine.bouih@uit.ac.ma  
Phone: +212 689 901 363    
"""

        # Build message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Bewerbung und Anfrage zur Ausbildung als Fachinformatiker für Anwendungsentwicklung"
        msg.attach(MIMEText(body, 'plain'))

        # Attach PDF
        with open(PDF_PATH, 'rb') as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(PDF_PATH))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(PDF_PATH)}"'
        msg.attach(part)

        # Send email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            print(f"✅ Sent to {email}")
        except Exception as e:
            print(f"❌ Failed to send to {email}: {e}")

        time.sleep(300)  # Avoid spam flags 5 min...