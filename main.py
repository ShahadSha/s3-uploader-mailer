import boto3
import os
from os.path import join, dirname
from botocore.exceptions import ClientError
import logging
import sys
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from validate_email import validate_email

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Creating the low level functional client
client = boto3.client(
    's3',
    aws_access_key_id = os.environ.get("aws_access_key_id"),
    aws_secret_access_key = os.environ.get("aws_secret_access_key"),
    region_name = os.environ.get("region_name"),
)

file_name = sys.argv[2]
expirey_time = int(sys.argv[1]) * 60
expirey_time_in_minutes = int(expirey_time) / 60
to_emails = sys.argv[3]
bucket = os.environ.get("bucket")
object_name = os.environ.get("object_name")
default_mail = os.environ.get("default_mail")
from_mail = os.environ.get("from_mail")
smtp_email = os.environ.get("from_mail")
smtp_pass = os.environ.get("smtp_pass")

def upload_file(file_name, bucket, expirey_time, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        file_upload = client.upload_file(file_name, bucket, object_name)
        response = client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': object_name}, ExpiresIn=expirey_time)
        
    except ClientError as e:
        logging.error(e)
        return False
    return response

file_link = upload_file(file_name, bucket, expirey_time, object_name)

# MAIL SECTION
email_list = to_emails.split(',')


def email_filter(email_list):
    filtered_emails = []
    for i in email_list:
        is_valid = validate_email(
            email_address=i,
            check_format=True,
            check_blacklist=True,
            check_dns=True,
            dns_timeout=10,
            check_smtp=True,
            smtp_timeout=10,
            smtp_helo_host='my.host.name',
            smtp_from_address='my@from.addr.ess',
            smtp_skip_tls=False,
            smtp_tls_context=None,
            smtp_debug=False,
        )
        print(i,is_valid,"okay")
        if (is_valid == True):
            filtered_emails.append(i)

    if ( len(filtered_emails) == 0 ) :
        filtered_emails.append(default_mail)
    return filtered_emails

filtered_emails = email_filter(email_list)
listToStr = ' '.join([str(elem) for i,elem in enumerate(filtered_emails)])

# EMAIL
msg = EmailMessage()
msg['Subject'] = file_name
msg['From'] = from_mail
msg['To'] = ", ".join(filtered_emails)

msg.set_content("Test Mesage")
html_message = open('mail.html').read()

## Replacing the values inside the html with the variable values
html_message = html_message.replace('{{filename}}',file_name).replace('{{download_link}}',file_link).replace('{{filtered_emails}}',listToStr).replace('{{expirey_time}}',str(expirey_time_in_minutes))
msg.add_alternative(html_message, subtype='html')


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(smtp_email, smtp_pass)
    smtp.send_message(msg)
    smtp.quit()

