import boto3
import hashlib

from botocore.client import Config
from pymongo import MongoClient
from pymongo.bulk import ObjectId
from datetime import date, datetime
import logging
from botocore.exceptions import ClientError
import os

from settings.settings import MONGO_PASS, MONGO_DB, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME



def get_database(db_name, collection_name):
    client = MongoClient(CONNECTION_STRING, connect=False)
    return client[db_name][collection_name]



def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True