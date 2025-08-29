import boto3

# Initialize EC2 client (uses default region from AWS config)
ec2 = boto3.client('ec2')

def main():
    # Get all running instances
    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )

    running_instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            launch_time = instance['LaunchTime']
            name = None
            # Get "Name" tag if present
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
            running_instances.append({
                "InstanceId": instance_id,
                "Name": name,
                "Type": instance_type,
                "LaunchTime": launch_time
            })

    if running_instances:
        print("Currently running instances:")
        for inst in running_instances:
            print(
                f"ID: {inst['InstanceId']} | "
                f"Name: {inst['Name']} | "
                f"Type: {inst['Type']} | "
                f"Launched: {inst['LaunchTime']}"
            )
    else:
        print("No running instances found.")

if __name__ == "__main__":
    main()
