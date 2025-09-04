# Author: Shubhk
import os
import json
import boto3

lambda_client = boto3.client('lambda')

LOADER_LAMBDA_NAME = os.environ.get('LOADER_LAMBDA_NAME')

def lambda_handler(event, context):
    print("Transformer Lambda triggered by event:", json.dumps(event))

    transformed_data = []
    for item in event:
        # Example transformation: Add a timestamp and a new field
        item['transformed_at'] = os.environ.get('CURRENT_TIMESTAMP', 'N/A') # Placeholder for actual timestamp
        item['status'] = 'processed'
        transformed_data.append(item)

    print(f"Transformed {len(transformed_data)} items. Invoking Loader Lambda.")

    # Invoke Loader Lambda
    if LOADER_LAMBDA_NAME:
        lambda_client.invoke(
            FunctionName=LOADER_LAMBDA_NAME,
            InvocationType='Event', # Asynchronous invocation
            Payload=json.dumps(transformed_data)
        )
        print(f"Successfully invoked Loader Lambda: {LOADER_LAMBDA_NAME}")
    else:
        print("LOADER_LAMBDA_NAME environment variable not set. Skipping invocation.")

    return {
        'statusCode': 200,
        'body': json.dumps('Transformer Lambda finished processing.')
    }
