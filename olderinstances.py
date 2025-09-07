import boto3
from datetime import datetime, timezone, timedelta

def find_old_instances(region="us-east-1"):
    ec2 = boto3.client("ec2", region_name=region)
    
    # Get all instances
    response = ec2.describe_instances()
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=180)
    
    old_instances = []
    
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            launch_time = instance["LaunchTime"]
            if launch_time < cutoff_date:
                # Extract Name tag if available
                name = None
                if "Tags" in instance:
                    for tag in instance["Tags"]:
                        if tag["Key"] == "Name":
                            name = tag["Value"]
                            break
                
                instance_info = {
                    "InstanceId": instance["InstanceId"],
                    "Name": name if name else "N/A",
                    "LaunchTime": str(launch_time),
                    "State": instance["State"]["Name"],
                    "InstanceType": instance["InstanceType"],
                    "Region": region
                }
                old_instances.append(instance_info)
    
    return old_instances

if __name__ == "__main__":
    region = "us-east-1"
    old_instances = find_old_instances(region)
    
    if old_instances:
        print(f"Instances older than 1 year in {region}:")
        for inst in old_instances:
            print(inst)
        print(f"\nTotal old instances in {region}: {len(old_instances)}")
    else:
        print(f"No instances older than 1 year in {region}")
