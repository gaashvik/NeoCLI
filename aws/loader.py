# Author: Shubhk
import json
import boto3

s3 = boto3.client('s3')

DESTINATION_BUCKET_NAME = os.environ.get('DESTINATION_BUCKET_NAME')

def lambda_handler(event, context):
    print("Loader Lambda triggered by event:", json.dumps(event))

    # In a real scenario, you would load this data into a database, data warehouse, or another S3 bucket.
    # For this example, we'll just print the data and simulate writing to S3.
    if event:
        print(f"Received {len(event)} items to load.")
        # Simulate writing to S3
        if DESTINATION_BUCKET_NAME:
            output_file_key = f"processed_data/{context.aws_request_id}.json"
            try:
                s3.put_object(
                    Bucket=DESTINATION_BUCKET_NAME,
                    Key=output_file_key,
                    Body=json.dumps(event, indent=2),
                    ContentType='application/json'
                )
                print(f"Successfully loaded data to s3://{DESTINATION_BUCKET_NAME}/{output_file_key}")
            except Exception as e:
                print(f"Error writing to S3 bucket {DESTINATION_BUCKET_NAME}: {e}")
                raise e
        else:
            print("DESTINATION_BUCKET_NAME environment variable not set. Skipping S3 write.")

    return {
        'statusCode': 200,
        'body': json.dumps('Loader Lambda finished processing.')
    }
