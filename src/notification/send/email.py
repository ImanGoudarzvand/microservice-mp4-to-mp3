import smtplib, os, json
from email.message import EmailMessage

def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("ADMIN_EMAIL")
        # sender_password = os.environ.get("ADMIN_PASSWORD")
        receiver_address = message["email"]


        msg = EmailMessage()
        msg.set_content(f"mp3 file_id: {mp3_fid} is now ready.")
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = receiver_address
        print("msg", msg)
        SMTP_HOST = os.environ["SMTP_HOST"]
        session = smtplib.SMTP(SMTP_HOST, 25)
        print("session", session)
        # session.starttls()
        # session.login(sender_address, sender_password)
        session.send_message(msg, sender_address, receiver_address)
        session.quit()
        print("Mail Sent")

    except Exception as err:
        # print('here error')
        # print(err)
        return err

