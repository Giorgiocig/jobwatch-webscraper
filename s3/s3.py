import json

import boto3
from botocore.client import Config

from helpers.helpers import load_config_from_env


def insert_data_to_s3(website, result_arr):
    config = load_config_from_env()

    aws_config = config["aws"]
    bucket_name = aws_config["bucket_name"]
    access_key = aws_config["access_key"]
    secret_key = aws_config["secret_key"]
    s3_config = config["s3"]
    endpoint_url = s3_config["endpoint_url"]

    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
        region_name="fr-par",
    )
    # Ensure result_arr is provided
    if not result_arr:
        print("No data to upload.")
        return
    for item in result_arr:
        item_data = json.dumps(item)
        unique_id = item["id"]
        # Define the object key using the format {provider}_{uniqueId}
        object_key = f"{website}_{unique_id}"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=item_data,
        )


def list_objects_in_the_bucket():
    config = load_config_from_env()

    aws_config = config["aws"]
    bucket_name = aws_config["bucket_name"]
    access_key = aws_config["access_key"]
    secret_key = aws_config["secret_key"]
    s3_config = config["s3"]
    endpoint_url = s3_config["endpoint_url"]

    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
        region_name="fr-par",
    )
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    for obj in response.get("Contents", []):
        print(obj["Key"])


def delete_item_from_S3(item_id):
    config = load_config_from_env()

    aws_config = config["aws"]
    bucket_name = aws_config["bucket_name"]
    access_key = aws_config["access_key"]
    secret_key = aws_config["secret_key"]
    s3_config = config["s3"]
    endpoint_url = s3_config["endpoint_url"]

    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
        region_name="fr-par",
    )
    response = s3_client.delete_object(Bucket=bucket_name, Key=f"{item_id}")
    print(f"Deleted from {bucket_name}")

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    for obj in response.get("Contents", []):
        print(obj["Key"])
