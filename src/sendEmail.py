import logging
import os
from datetime import datetime

import yagmail

import log


class Email:
    def __init__(self, userGmail, target_username, targetGmail, messageList, downloadPath):
        self.gmail = userGmail
        self.target_username = target_username
        self.subject = f"WhatsApp Notification From {target_username} "
        self.messageList = messageList
        self.targetGmail = targetGmail
        self.attach_list = []
        self.downloadPath = downloadPath
        self.now = datetime.now()
        logging.debug("__init__ is initiated")

    def initYagmail(self):
        try:
            yag = yagmail.SMTP(self.gmail)
            logging.debug("Successfully initiated yagmail SMTP connection")
            return yag
        except Exception as e:
            error = f"Failed to initiate connection: {e}"
            logging.error(error)

    def get_attach_list(self):
        with os.scandir(self.downloadPath) as entries:
            for entry in entries:
                if entry.is_file():
                    self.attach_list.append(os.path.join(self.downloadPath, entry.name))
                    logging.debug(f"file {entry.name} is found")

    def send_email(self):
        yag = Email.initYagmail(self)
        date = self.now.strftime("%d/%m/%Y %H:%M:%S")
        subject_title = self.subject + date
        try:
            yag.send(
                to = self.targetGmail,
                subject = subject_title,
                contents = self.messageList,
                attachments = self.attach_list
            )
            logging.info(f"Email is sent to {self.target_username}")
            self.send_logfile(date, yag)
        except Exception as e:
            logging.error(f"Failed to send email to {self.target_username}: {e}")

    def send_logfile(self, date, yag):
        LogPath = log.userLog_path
        subjectTitle = f"Log File of WhatsMail at {date}"
        try:
            log.stopLogging()
            yag.send(
                to=self.gmail,
                subject=subjectTitle,
                contents="log file",
                attachments=LogPath
            )
        except Exception as e:
            try:
                logging.critical(f"Failed to send log file: {e}")
            except Exception:
                pass

def sendGmail(userGmail, target_username, targetGmail, messageList, downloadPath):
    email = Email(userGmail, target_username, targetGmail, messageList, downloadPath)
    email.initYagmail()
    email.get_attach_list()
    email.send_email()

