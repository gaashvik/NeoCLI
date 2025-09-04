
# Author: Shubhk
import json
import boto3

s3 = boto3.client('s3')

def handler(event, context):
    # The body from the previous lambda is a JSON string of the transformed data
    transformed_data = json.loads(event['body'])

    target_bucket_name = 'sentinal-ai-etl-output'  # Define your target S3 bucket name
    output_file_key = 'processed_data.json'

    print(f"Loading {len(transformed_data)} records to s3://{target_bucket_name}/{output_file_key}")

    try:
        s3.put_object(
            Bucket=target_bucket_name,
            Key=output_file_key,
            Body=json.dumps(transformed_data, indent=2),
            ContentType='application/json'
        )
        print("Data loaded successfully.")
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data loaded successfully'})
        }
    except Exception as e:
        print(f"Error loading data to S3: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error loading data: {e}'})
        }
