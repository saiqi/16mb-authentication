from flask_mail import Mail, Message

mail = Mail()

def send_mail(recipient, subject, body):
    recipients = recipient
    if not isinstance(recipient, list):
        recipients = [recipient]
    msg = Message(subject=subject, recipients=recipients, body=body)
    mail.send(msg)
