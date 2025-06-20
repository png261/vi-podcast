import boto3
import os
import io
import mimetypes
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Load and validate required environment variables
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_REGION = os.getenv("R2_REGION", "auto")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
BASE_URL_S3 = os.getenv("BASE_URL_S3")

if not all([R2_ENDPOINT_URL, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME, BASE_URL_S3]):
    raise EnvironmentError(
        "Missing one or more required R2 environment variables.")

# Setup S3 (R2-compatible) client
s3_client = boto3.client(
    service_name="s3",
    endpoint_url=R2_ENDPOINT_URL,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name=R2_REGION,
)


def upload_file(file_content: bytes, file_key: str, content_type: str = None) -> str:
    """
    Upload a file to Cloudflare R2 and return its public URL.
    Automatically sets Content-Type based on file extension if not provided.
    """
    # Guess MIME type if not explicitly set
    if content_type is None:
        content_type, _ = mimetypes.guess_type(file_key)
    if not content_type:
        content_type = "application/octet-stream"

    try:
        s3_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=file_key,
            Body=file_content,
            ContentType=content_type
        )
        return f"{BASE_URL_S3.rstrip('/')}/{file_key}"
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
