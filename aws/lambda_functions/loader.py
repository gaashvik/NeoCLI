
import json
import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Loader Lambda triggered by event:", json.dumps(event))

    detail = json.loads(event['detail'])
    source_bucket = detail['bucket']
    source_key = detail['key']

    print(f"Processing file {source_key} from bucket {source_bucket}")

    try:
        # Get the transformed JSON data from S3
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        transformed_data = json.loads(response['Body'].read().decode('utf-8'))

        # Define output bucket and key for loaded data
        # For this example, we'll just store it in an S3 bucket, but in a real scenario,
        # this could be loading into a database (DynamoDB, Redshift, etc.)
        output_bucket = os.environ.get('LOADED_DATA_BUCKET')
        output_key = f"loaded/{source_key.split('/')[-1]}"

        # Upload loaded data to S3
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=json.dumps(transformed_data),
            ContentType='application/json'
        )
        print(f"Successfully loaded data to {output_bucket}/{output_key}")

    except Exception as e:
        print(f"Error processing file {source_key}: {e}")
        raise e
