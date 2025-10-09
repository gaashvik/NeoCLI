
import json
import csv
import boto3
import os

s3 = boto3.client('s3')

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

            # Parse CSV
            reader = csv.DictReader(csv_content.splitlines())
            
            extracted_data = []
            for row in reader:
                extracted_data.append(row)

            # Define output bucket and key
            output_bucket = os.environ.get('EXTRACTED_DATA_BUCKET')
            output_key = f"extracted/{file_key.replace('.csv', '.json')}"

            # Upload extracted data as JSON to another S3 bucket
            s3.put_object(
                Bucket=output_bucket,
                Key=output_key,
                Body=json.dumps(extracted_data),
                ContentType='application/json'
            )
            print(f"Successfully extracted and uploaded {output_key} to {output_bucket}")

            # Publish an EventBridge event to trigger the transformer
            eventbridge = boto3.client('events')
            eventbridge.put_events(
                Entries=[
                    {
                        'Source': 'com.mycompany.etl',
                        'DetailType': 'ExtractedDataReady',
                        'Detail': json.dumps({
                            'bucket': output_bucket,
                            'key': output_key
                        }),
                        'EventBusName': 'default'
                    }
                ]
            )
            print(f"Published EventBridge event for {output_key}")

        except Exception as e:
            print(f"Error processing file {file_key}: {e}")
            raise e

