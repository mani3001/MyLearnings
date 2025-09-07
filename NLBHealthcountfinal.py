import boto3
import datetime
import time
import requests
import re

# ==== CONFIGURATION ====
DT_ENV_URL = "xxxx"
DT_API_TOKEN = "xxxx"
NLB_NAME = "net/DynatraceNLB/eebca1152be1dbbd"
TARGET_GROUP = "targetgroup/DynatraceLBInstance/43213e1f76deec36"
REGION = "us-east-1"

# AWS CloudWatch client
cloudwatch = boto3.client("cloudwatch", region_name=REGION)

# ==== FETCH METRIC FROM CLOUDWATCH ====
end = datetime.datetime.now(datetime.timezone.utc)
start = end - datetime.timedelta(minutes=10)

response = cloudwatch.get_metric_statistics(
    Namespace="AWS/NetworkELB",
    MetricName="HealthyHostCount",
    Dimensions=[
        {"Name": "TargetGroup", "Value": TARGET_GROUP},
        {"Name": "LoadBalancer", "Value": NLB_NAME}
    ],
    StartTime=start,
    EndTime=end,
    Period=60,
    Statistics=["Average"]
)

datapoints = response.get("Datapoints", [])
if not datapoints:
    print("No HealthyHostCount data found")
    exit(0)

latest = sorted(datapoints, key=lambda x: x["Timestamp"])[-1]
value = latest.get("Average")
if value is None:
    print("Datapoint has no Average:", latest)
    exit(0)

value = float(value)
timestamp = int(time.time() * 1000)

# ==== SANITIZE DIMENSIONS ====
def sanitize(s: str) -> str:
    return re.sub(r'[^A-Za-z0-9_\-.:]', "_", s)

lb_label = sanitize(NLB_NAME)
tg_label = sanitize(TARGET_GROUP)

# ==== BUILD METRIC LINE ====
metric_line = (
    f"aws.networkelb.healthyhostcount,"
    f"loadbalancer={lb_label},"
    f"targetgroup={tg_label},"
    f"region={REGION} "
    f"{value} {timestamp}"
)

print("Metric line:", metric_line)

# ==== SEND TO DYNATRACE ====
url = f"{DT_ENV_URL}/api/v2/metrics/ingest"
headers = {
    "Authorization": f"Api-Token {DT_API_TOKEN}",
    "Content-Type": "text/plain; charset=utf-8"
}

resp = requests.post(url, headers=headers, data=metric_line)
print("Dynatrace response:", resp.status_code, resp.text)
