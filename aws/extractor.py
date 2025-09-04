
import os
import json
import csv
import boto3

s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')

TRANSFORMER_LAMBDA_NAME = os.environ.get('TRANSFORMER_LAMBDA_NAME')

def lambda_handler(event, context):
    print("Extractor Lambda triggered by event:", json.dumps(event))

    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']

        print(f"Processing file {file_key} from bucket {bucket_name}")

        try:
            # Get the CSV file from S3
            response = s3.get_object(Bucket=bucket_name, Key=file_key)
            csv_content = response['Body'].read().decode('utf-8')

            # Parse CSV and prepare for transformer
            lines = csv_content.strip().split('\n')
            csv_reader = csv.reader(lines)
            header = next(csv_reader) # Skip header or use it for mapping

            data_to_transform = []
            for i, row in enumerate(csv_reader):
                if row: # Ensure row is not empty
                    # Assuming CSV has 3 columns: id, name, value
                    item = {
                        'id': row[0],
                        'name': row[1],
                        'value': int(row[2]) # Convert value to int
                    }
                    data_to_transform.append(item)

            print(f"Extracted {len(data_to_transform)} items. Invoking Transformer Lambda.")

            # Invoke Transformer Lambda
            if TRANSFORMER_LAMBDA_NAME:
                lambda_client.invoke(
                    FunctionName=TRANSFORMER_LAMBDA_NAME,
                    InvocationType='Event', # Asynchronous invocation
                    Payload=json.dumps(data_to_transform)
                )
                print(f"Successfully invoked Transformer Lambda: {TRANSFORMER_LAMBDA_NAME}")
            else:
                print("TRANSFORMER_LAMBDA_NAME environment variable not set. Skipping invocation.")

        except Exception as e:
            print(f"Error processing file {file_key}: {e}")
            raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Extractor Lambda finished processing.')
    }
