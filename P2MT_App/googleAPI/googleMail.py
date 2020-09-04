# Stuff for Google Mail functions

from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import base64
from google.oauth2 import service_account

# Email variables. Modify this!
EMAIL_FROM = "phase2team@students.hcde.org"
EMAIL_TO = "phase2team@students.hcde.org"
EMAIL_SUBJECT = "STEM Intervention"
EMAIL_CONTENT = "STEM Intervention Email Content"


def create_message(sender, to, subject, message_text):
    """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
  Returns:
    An object containing a base64url encoded email object.
  """
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {"raw": raw}
    return {"raw": raw}


def send_message(service, user_id, message):
    """Send an email message.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
  Returns:
    Sent Message.
  """
    try:
        message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        print("Message Id: %s" % message["id"])
        return message
    except errors.HttpError as error:
        print("An error occurred: %s" % error)


def service_account_login():
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    SERVICE_ACCOUNT_FILE = (
        "../../google_credentials/verdant-root-256217-566d3ff37798.json"
    )

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    delegated_credentials = credentials.with_subject(EMAIL_FROM)
    service = build("gmail", "v1", credentials=delegated_credentials)
    return service


service = service_account_login()
# Call the Gmail API
message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
print("message =", message)
sent = send_message(service, "me", message)
