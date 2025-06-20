import boto3
import os
import io
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Setup S3 (R2-compatible) client
s3_client = boto3.client(
    service_name="s3",
    endpoint_url=os.getenv("R2_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
    region_name=os.getenv("R2_REGION", "auto"),
)

R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")


def upload_file(file_content: bytes, file_key: str) -> str:
    """
    Upload a file to Cloudflare R2.
    Returns the public URL if successful.
    """
    try:
        s3_client.upload_fileobj(io.BytesIO(
            file_content), R2_BUCKET_NAME, file_key)
        return f"{os.getenv('BASE_URL_S3')}/{file_key}"

    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to upload to R2: {e}")


def get_file_info(file_key: str) -> dict:
    """
    Get metadata about a file stored in R2.
    """
    try:
        return s3_client.head_object(Bucket=R2_BUCKET_NAME, Key=file_key)
    except ClientError as e:
        raise RuntimeError(f"Failed to retrieve file info: {e}")
