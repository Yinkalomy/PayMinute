import boto3

access_key = 'AKIA27SYJJBR2RB2PWIU'
secret_key = '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'

bucket_name='payminutelomy'
region ='ca-central-1'


def create_bucket():
    client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
    )


    client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint':region
                }
            )