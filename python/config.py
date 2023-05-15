import logging
import os
import boto3
import base64
from botocore.exceptions import ClientError

logger = logging.getLogger()

ENVIRONMENT = os.environ["Environment"]
PROJECT = os.environ["Project"]
ACCESS_TOKEN = "ACCESS_TOKEN-" + PROJECT + "-" + ENVIRONMENT


def get_secret():
    session = boto3.session.Session()
    sm = session.client(service_name="secretsmanager", region_name="eu-west-1")
    secret = None

    try:
        get_secret_value_response = sm.get_secret_value(SecretId=ACCESS_TOKEN)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])

    return secret
