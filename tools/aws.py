import os
import json

import boto3
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())


class S3:
    def __init__(self) -> None:
        self.bucket_name = 'bucket_name'
        self.aws_access_key_id = os.getenv("aws_access_key_id")
        self.aws_secret_access_key = os.getenv("aws_secret_access_key")

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def list_buckets(self):
        buckets = self.s3_client.list_buckets()
        print(buckets)

    def get_bucket_policy(self, bucket_name):
        policy = self.s3_client.get_bucket_policy(Bucket=bucket_name)
        print(policy['Policy'])

    def set_bucket_policy(self, bucket_name: str) -> None:
        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'AddPerm',
                    'Effect': 'Allow',
                    'Principal': '*',
                    'Action': ['s3:GetObject'],
                    'Resource': f'arn:aws:s3:::{bucket_name}/*',
                }
            ],
        }
        bucket_policy = json.dumps(bucket_policy)

        self.get_bucket_policy(bucket_name)
        self.s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        self.get_bucket_policy(bucket_name)

    def delete_bucket_policy(self, bucket_name: str) -> None:
        self.s3_client.delete_bucket_policy(Bucket=bucket_name)


if __name__ == '__main__':
    s3 = S3()
    print("Setting policy...")
    s3.set_bucket_policy()
    input("Press ENTER to delete policy...")
    s3.delete_bucket_policy()
    print("DONE")
