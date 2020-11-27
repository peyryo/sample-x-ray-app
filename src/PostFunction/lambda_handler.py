import json
from datetime import datetime

import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all


patch_all()

RESOURCE_PREFIX = "x-ray-sample"


@xray_recorder.capture('parse_event')
def parse_event(event):

    body = json.loads(event["body"])
    path_params = event["pathParameters"]

    if body is None or path_params is None:
        raise Exception

    text = body.get("text") or "No Text"
    user_id = path_params.get("user_id") or "No User"

    segment = xray_recorder.current_subsegment()
    segment.put_annotation('user_id', user_id)
    segment.put_metadata('text', text)
    
    return (user_id, text)


def put_todo(user_id, text):

    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table(RESOURCE_PREFIX + "-table")

    table.put_item(
        Item={
            "UserID": user_id,
            "CreateDate": datetime.utcnow().isoformat(),
            "text": text
        }
    )


def lambda_handler(event, context):

    try:

        (user_id, text) = parse_event(event)

        put_todo(user_id, text)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Success",
            })
        }

    except Exception as e:
        print(e)

        return {
            "statusCode": 500,
            "body": json.dumps({
               "message": "Internal Server Error",
            })
        }