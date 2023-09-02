import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(file_path, s3_key, bucket_name):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
    except NoCredentialsError:
        print("Credentials not available")

def download_data_from_s3(bucket_name, remote_folder, local_folder):
    s3 = boto3.client('s3')
    print(bucket_name)
    try:
        s3.download_file(bucket_name, f'{remote_folder}/train-images-idx3-ubyte.gz', f'{local_folder}/train-images-idx3-ubyte.gz')
        s3.download_file(bucket_name, f'{remote_folder}/train-labels-idx1-ubyte.gz', f'{local_folder}/train-labels-idx1-ubyte.gz')
        s3.download_file(bucket_name, f'{remote_folder}/t10k-images-idx3-ubyte.gz', f'{local_folder}/t10k-images-idx3-ubyte.gz')
        s3.download_file(bucket_name, f'{remote_folder}/t10k-labels-idx1-ubyte.gz', f'{local_folder}/t10k-labels-idx1-ubyte.gz')
    except NoCredentialsError:
        print("Credentials not available")
