from smtplib import SMTP_SSL
from email.message import EmailMessage


class EmailDispacher:
    def __init__(
        self, email_address, email_password, destination_email, subject, content = None, attachment = None
    ) -> None:
        self.email_address = email_address
        self.email_password = email_password
        self.destination_email = destination_email
        self.subject = subject
        self.content = content
        self.attachment = attachment
    

    def execute(self):
        msg = self.configSender()
        self.sendMail(msg)


    def configSender(self):
        msg = EmailMessage()
        msg["Subject"] = self.subject
        msg["From"] = self.email_address
        msg["To"] = self.destination_email
        msg.set_content(self.content, subtype="html")

        if self.attachment:
            try:
                filename = self.attachment.split('/')[-1]
                with open(self.attachment, "rb") as file:
                    msg.add_attachment(
                        file.read(),
                        maintype="application",
                        subtype="octet-stream",
                        filename=filename,
                    )
            except Exception as e:
                raise Exception("Error: ", e)

        return msg


    def sendMail(self, msg):
        try:
            with SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)
        except Exception as e:
            raise Exception("Error: ", e)
