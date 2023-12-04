import json
import boto3
from discordwebhook import Discord
import time
import os

def lambda_handler(event, context):
  cloudwatch = boto3.client('cloudwatch')

  metrics = {
    "Invocations": [
      [ "AWS/Lambda", "Invocations", "FunctionName", "funtion1", { "period": 900, "stat": "Sum", "region": "ap-northeast-1" } ],
      [ "...", "funtion2", { "period": 900, "stat": "Sum", "region": "ap-northeast-1" } ],
      [ "...", "funtion3", { "period": 900, "stat": "Sum", "region": "ap-northeast-1" } ],
      [ "...", "funtion4", { "period": 900, "stat": "Sum", "region": "ap-northeast-1" } ]
    ],
    "Errors": [
      [ "AWS/Lambda", "Errors", "FunctionName", "funtion1", { "period": 300, "stat": "Sum", "region": "ap-northeast-1" } ],
      [ "...", "funtion2", { "period": 300, "stat": "Sum", "region": "ap-northeast-1" } ],
      [ "...", "funtion3", { "period": 300, "stat": "Sum", "region": "ap-northeast-1" } ],
      [ "...", "funtion4", { "period": 300, "stat": "Sum", "region": "ap-northeast-1" } ]
    ],
    "Duration": [
      [ "AWS/Lambda", "Duration", "FunctionName", "funtion1", { "period": 300, "stat": "Average", "region": "ap-northeast-1" } ],
      [ "...", "funtion2", { "period": 300, "stat": "Average", "region": "ap-northeast-1" } ],
      [ "...", "funtion3", { "period": 300, "stat": "Average", "region": "ap-northeast-1" } ],
      [ "...", "funtion4", { "period": 300, "stat": "Average", "region": "ap-northeast-1" } ]]
    ],
  }

  for metric, _ in metrics.items():

    widget_definition = json.dumps(
      {
        "liveData": False,
        "stacked": False,
        "width": 800,
        "height": 400,
        "start": '-PT3H',
        "end": "P0D",
        "timezone": '+0900',
        "view": "timeSeries",
        "metrics": metrics[metric],
      }
    )

    response = cloudwatch.get_metric_widget_image(MetricWidget = widget_definition)
    image_path = f'/tmp/{metric}.png'

    time.sleep(1)

    with open (image_path, 'wb') as f:
      f.write(response["MetricWidgetImage"])

    webhook_url = os.getenv('discord_webhook_url')

    discord = Discord(url=webhook_url)
    with open(image_path, 'rb') as f:
      discord.post(username="monitoring", content=metric, file={ "attachment": f })
  
  return {
    'statusCode': 200,
    'body': json.dumps('Hello from Lambda!')
  }
