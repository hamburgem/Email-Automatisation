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
EMAIL_PASSWORD = getpass.getpass("🔐 Enter your 16-digit App Password (not your Gmail password): ")

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
        name = row.get('Name', '').strip()
        email = row.get('Email', '').strip()

        if not name or not email:
            print("⚠️ Skipping row with missing data:", row)
            continue

        print(f"📤 Preparing to send to: {name} ({email})")

        # Email body
        body = f"""Sehr geehrtes Team der {name},

ich hoffe, diese Nachricht erreicht Sie wohlbehalten.

Mein Name ist Yassin Bouih und ich befinde mich derzeit im dritten Jahr meines Bachelorstudiums im Bereich Künstliche Intelligenz an der Ibn Tofail Universität in Marokko. Ich rechne mit meinem Abschluss im Juli 2026 und einem Notendurchschnitt von etwa 13/20 (entspricht ca. 2,6–3,5). Derzeit bereite ich mich auf die B2-Prüfung in Deutsch (ÖSD) vor, die ich bis Januar 2026 abschließen möchte. Außerdem plane ich, Anfang 2026 die IELTS-Prüfung in Englisch abzulegen.

Ich interessiere mich sehr für den Masterstudiengang Data Science und Künstliche Intelligenz zum Wintersemester 2026 und wäre Ihnen dankbar, wenn Sie mir folgende Fragen beantworten könnten:

Bewerbungszeitraum:
Wann beginnt und endet die Bewerbungsfrist für internationale Studierende für das Wintersemester 2026?
Kann ich mich mit einem vorläufigen Zeugnis bewerben, obwohl mein Abschluss noch aussteht?
Ist es möglich, sich zu bewerben, auch wenn das B2-Zertifikat noch nicht vorliegt, und dieses vor der Immatrikulation nachzureichen?

Zulassungsvoraussetzungen:
Reicht ein B2-Zertifikat (ÖSD) aus oder wird DSH/TestDaF zwingend verlangt?
Gibt es eine Mindestnote für Bewerber*innen aus Marokko?

Bewerbungsprozess:
Läuft die Bewerbung über Uni-Assist oder direkt über Ihre Hochschule?
Wann werden die Zulassungsentscheidungen in der Regel bekanntgegeben?

Gerne sende ich Ihnen bei Bedarf meinen Lebenslauf als PDF zur ersten Durchsicht zu.

Ich danke Ihnen herzlich für Ihre Zeit und Unterstützung und freue mich auf Ihre Rückmeldung.

Mit freundlichen Grüßen
Yassin Bouih
Email: yassine.bouih@uit.ac.ma  
Phone: +212 6 89 9013 63  
Current University: Ibn Tofail University, Morocco  
Expected Graduation: July 2026  
"""

        # Build message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Anfrage zum Masterstudiengang Data Science und Künstliche Intelligenz – Wintersemester 2026"
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

        time.sleep(540)  # Avoid spam flags 5 min...