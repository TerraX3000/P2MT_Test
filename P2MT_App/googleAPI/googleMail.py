# Stuff for Google Mail functions

from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import base64
from google.oauth2 import service_account
from P2MT_App.main.referenceData import getSystemAccountEmail, getEmailModeStatus
from flask_login import current_user
import json

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
    print("Running send_message()")
    try:
        message = (
            service.users().messages().send(userId=user_id, body=message).execute()
        )
        print("Message Id: %s" % message["id"])
        return message
    except:
        print("Error occurred")
        # except errors.HttpError as error:
        print("An error occurred: %s" % errors)
        print("error code: ", errors.HttpError)


def service_account_login():
    print("Running service_account_login()")
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    # SCOPES = ["https://www.googleapis.com/auth/sqlservice.admin"]
    # SCOPES = ["https://www.googleapis.com/auth/calendar"]
    # SCOPES = ["https://www.googleapis.com/auth/tasks"]
    SERVICE_ACCOUNT_FILE = "google_credentials/verdant-root-256217-566d3ff37798.json"

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    print(
        "credentials.project_id =", credentials.project_id,
    )
    print(
        "credentials._service_account_email =", credentials._service_account_email,
    )
    print(
        "credentials.scopes =", credentials.scopes,
    )
    print(
        "credentials.expired =", credentials.expired,
    )
    print(
        "credentials.valid =", credentials.valid,
    )
    delegated_credentials = credentials.with_subject("phase2team@students.hcde.org")
    print(
        "delegated_credentials.project_id =", delegated_credentials.project_id,
    )
    print(
        "delegated_credentials._service_account_email =",
        delegated_credentials._service_account_email,
    )
    print(
        "delegated_credentials.scopes =", delegated_credentials.scopes,
    )
    print(
        "delegated_credentials.expired =", delegated_credentials.expired,
    )
    print(
        "delegated_credentials.valid =", delegated_credentials.valid,
    )

    # Create an httplib2.Http object to handle our HTTP requests and authorize
    # it with the Credentials.
    # http = Http()
    # http = credentials.authorize(http)

    # service = build("tasks", "v1", http=http)

    # # List all the tasklists for the account.
    # lists = service.tasklists().list().execute(http=http)
    # pprint.pprint(lists)

    service = build("gmail", "v1", credentials=delegated_credentials)

    # service = googleapiclient.discovery.build(
    #     "sqladmin", "v1beta4", credentials=credentials
    # )

    return service


# service = service_account_login()
# # Call the Gmail API
# message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
# print("message =", message)
# sent = send_message(service, "me", message)


def sendEmail(email_to, email_cc, emailSubject, emailContent):
    # include the system account as a bcc recipient on all emails
    email_bcc = getSystemAccountEmail()
    # if the email recipient is a list, then use commas to seperate the email addresses
    if isinstance(email_to, list):
        email_to = ",".join(email_to)
    # Retrieve current system mode
    SystemMode = getEmailModeStatus()
    if SystemMode == False:
        print("System Mode = Test. Sending email to", current_user.email)
        email_to = current_user.email
        email_cc = current_user.email
    print(email_to, email_cc, email_bcc, emailSubject, emailContent)
    message = create_message(email_to, email_cc, emailSubject, emailContent)
    print("message =", message)
    service = service_account_login()
    print("service =", service)
    print("service json =", json.dumps(service, indent=4, separators=("", " = ")))
    # print("service resource =", service["resources"])
    # sent = send_message(service, "me", message)
    # print("sent message =", sent)
    return

