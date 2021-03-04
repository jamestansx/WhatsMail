import yagmail
import os

class Email:
    def __init__(self, userGmail, target_username, targetGmail, messageList, downloadPath):
        self.gmail = userGmail
        self.target_username = target_username
        self.subject = f"WhatsApp Notification From {target_username}"
        self.messageList = messageList
        self.targetGmail = targetGmail
        self.attach_list = []
        self.downloadPath = downloadPath

    def initYagmail(self):
        try:
            yag = yagmail.SMTP(self.gmail)
            return yag
        except Exception as e:
            error = f"Failed to initiate connection: {e}"
            print(error)

    def get_attach_list(self):
        with os.scandir(self.downloadPath) as entries:
            for entry in entries:
                if entry.is_file():
                    self.attach_list.append(os.path.join(self.downloadPath, entry.name))

    def send_email(self):
        yag = Email.initYagmail(self)
        try:
            yag.send(
                to = self.targetGmail,
                subject = self.subject,
                contents = self.messageList,
                attachments = self.attach_list
            )
            print(f"Email is sent to {self.target_username}")
        except Exception as e:
            print(f"Failed to send email to {self.target_username}: {e}")

def sendGmail(userGmail, target_username, targetGmail, messageList, downloadPath):
    email = Email(userGmail, target_username, targetGmail, messageList, downloadPath)
    email.initYagmail()
    email.get_attach_list()
    email.send_email()

