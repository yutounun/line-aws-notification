import os
import requests
import boto3
import datetime


def notify(event, context):
    client = boto3.client("ce")
    today = datetime.date.today()
    response = client.get_cost_and_usage(
        TimePeriod={
            "Start": today,
            "End": today,
        },
        Granularity="DAILY",
        Metrics=["BlendedCost"],
    )
    cost = response["ResultsByTime"][0]["Total"]["BlendedCost"]["Amount"]

    send_to_line(f"Today's AWS bill is ${round(cost, 2)} です。")


def send_to_line(message):
    url = os.environ["LINEPostURL"]
    token = os.environ["LINEtoken"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"message": message}
    requests.post(url, headers=headers, data=data)
