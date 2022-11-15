#!/usr/bin/env python

import logging
from config import get_secret
import json
from mastodon import Mastodon

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

secret = get_secret()

def lambda_handler(event, context):

    for record in event["Records"]:
        logging.info("record: " + record["body"])
        raw_record = record["body"]
        logging.info("raw_length: " + str(len(raw_record)))
        toot = (raw_record[:275] + "..") if len(raw_record) > 279 else raw_record
        logging.info("toot_length: " + str(len(toot)))
        logging.info("Publishing the queued toot: " + toot)
        mastodon = Mastodon(access_token=secret, api_base_url="https://botsin.space/")

        mastodon.status_post(toot)

    body = {"message": "ACK", "event": event}

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
