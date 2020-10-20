import boto3 as b3
from botocore.exceptions import ClientError
import logging

# Custom functions
import utils

# Format logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                            format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s')

class Email():
    def __init__(self):
        """Authenticate email server and prepare configuration"""
        # AWS access
        ACCESS_KEY = utils.get_secret("key_id", "aws")
        SECRET_KEY = utils.get_secret("secret", "aws")
        AWS_REGION = "eu-central-1"

        # Create a new SES resource and specify a region.
        self.client = b3.client('ses',
                            aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY,
                            region_name = AWS_REGION)

        # Sender, receiver
        self.SENDER = utils.get_secret("sender", "email")
        recipients = utils.get_secret("receiver", "email")
        self.RECEIVERS = recipients.split(",")

        # Config
        self.CHARSET = "UTF-8"

    def send(self, subject: str, body: str):
        """Append payload and send email"""
        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': self.RECEIVERS
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': self.CHARSET,
                            'Data': body,
                        },
                    },
                    'Subject': {
                        'Charset': self.CHARSET,
                        'Data': subject,
                    },
                },
                Source = self.SENDER,
            )
        except ClientError as e:
            log.error(e.response['Error']['Message'])
        else:
            log.info("Email sent! Message ID: %s" % response['MessageId']),