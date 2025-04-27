import os
import shutil
import smtplib
from email.mime.text import MIMEText
import schedule
import time
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

# Thông tin email
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Đường dẫn thư mục database và backup
DATABASE_DIR = "path/to/database"
BACKUP_DIR = "path/to/backup"

def dai_database():
    try:
        # Tạo thư mục backup nếu chưa có
        os.makedirs(BACKUP_DIR, exist_ok=True)

        backed_up_files = []
        for filename in os.listdir(DATABASE_DIR):
            if filename.endswith((".sql", ".sqlite3")):
                src = os.path.join(DATABASE_DIR, filename)
                dest = os.path.join(BACKUP_DIR, filename)
                shutil.copy2(src, dest)
                backed_up_files.append(filename)

        if backed_up_files:
            body = f"Đã backup thành công các file: {', '.join(backed_up_files)}."
            subject = "Backup Database Thành Công"
        else:
            body = "Không tìm thấy file .sql hoặc .sqlite3 để backup."
            subject = "Backup Database - Không có file"

        send_email(subject, body)
    except Exception as error:
        send_email("Backup Database Thất Bại", f"Lỗi: {error}")

def send_email(subject, content):
    message = MIMEText(content)
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECEIVER
    message["Subject"] = subject

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(message)
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

# Lên lịch backup lúc 00:00 mỗi ngày
schedule.every().day.at("00:00").do(dai_database)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
