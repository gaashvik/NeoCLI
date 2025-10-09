
import json
import boto3
import os
import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Transformer Lambda triggered by event:", json.dumps(event))

    detail = json.loads(event['detail'])
    source_bucket = detail['bucket']
    source_key = detail['key']

    print(f"Processing file {source_key} from bucket {source_bucket}")

    try:
        # Get the extracted JSON data from S3
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        extracted_data = json.loads(response['Body'].read().decode('utf-8'))

        transformed_data = []
        for row in extracted_data:
            # Example transformation: Add a timestamp and convert 'value' to integer
            row['processed_at'] = datetime.datetime.now().isoformat()
            try:
                row['value'] = int(row['value'])
            except (ValueError, TypeError):
                row['value'] = None # Handle cases where value might not be an integer
            transformed_data.append(row)

        # Define output bucket and key
        output_bucket = os.environ.get('TRANSFORMED_DATA_BUCKET')
        output_key = f"transformed/{source_key.split('/')[-1]}"

        # Upload transformed data as JSON to another S3 bucket
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=json.dumps(transformed_data),
            ContentType='application/json'
        )
        print(f"Successfully transformed and uploaded {output_key} to {output_bucket}")

        # Publish an EventBridge event to trigger the loader
        eventbridge = boto3.client('events')
        eventbridge.put_events(
            Entries=[
                {
                    'Source': 'com.mycompany.etl',
                    'DetailType': 'TransformedDataReady',
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
        print(f"Error processing file {source_key}: {e}")
        raise e
