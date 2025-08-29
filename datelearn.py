import boto3
from datetime import datetime, timezone, timedelta

# Initialize clients
iam = boto3.client('iam')

# Define cutoff
cutoff_date = datetime.now(timezone.utc) - timedelta(days=90)

def is_user_inactive(user):
    username = user['UserName']
    user_inactive = True

    # Check password last used
    if 'PasswordLastUsed' in user and user['PasswordLastUsed']:
        if user['PasswordLastUsed'] > cutoff_date:
            user_inactive = False

    # Check access keys
    keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
    for key in keys:
        last_used = iam.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])
        if 'LastUsedDate' in last_used['AccessKeyLastUsed']:
            if last_used['AccessKeyLastUsed']['LastUsedDate'] > cutoff_date:
                user_inactive = False

    return user_inactive

def main():
    print(f"Inactive users (no activity in last 365 days):\n{'-'*80}")
    paginator = iam.get_paginator('list_users')
    for page in paginator.paginate():
        for user in page['Users']:
            if is_user_inactive(user):
                password_last_used = user.get('PasswordLastUsed', None)
                print(
                    f"User: {user['UserName']} | "
                    f"Created: {user['CreateDate']} | "
                    f"PasswordLastUsed: {password_last_used}"
                )

if __name__ == "__main__":
    main()
