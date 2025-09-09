import boto3
import datetime

# Set your AWS region
REGION = "us-east-1"

# Create clients
ec2 = boto3.client("ec2", region_name=REGION)
cloudwatch = boto3.client("cloudwatch", region_name=REGION)

def get_instance_name(tags):
    """Extract Name tag if exists"""
    if tags:
        for tag in tags:
            if tag["Key"] == "Name":
                return tag["Value"]
    return "Unnamed"

def get_cpu_utilization(instance_id):
    """Fetch latest CPU utilization for an EC2 instance"""
    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(minutes=10)  # last 10 mins

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,  # 5 min interval
        Statistics=["Average"],
        Unit="Percent"
    )

    #print(response.get("Datapoints"))  # Debugging line to inspect the response

    datapoints = response.get("Datapoints", [])
    if datapoints:
        latest = sorted(datapoints, key=lambda x: x["Timestamp"])[-1]
        return round(latest["Average"], 2)
    return None

def main():
    # Get all running EC2 instances
    reservations = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )["Reservations"]

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_name = get_instance_name(instance.get("Tags", []))

            cpu_util = get_cpu_utilization(instance_id)
            if cpu_util is not None:
                print(f"Instance: {instance_name} ({instance_id}) - CPU Usage: {cpu_util}%")
            else:
                print(f"Instance: {instance_name} ({instance_id}) - No CPU data found")

if __name__ == "__main__":
    main()
