
import json
import boto3
import csv

s3 = boto3.client('s3')

def handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    print(f"Extracting data from s3://{bucket_name}/{file_key}")

    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read().decode('utf-8')
    
    # Assuming CSV content, parse it
    lines = content.strip().split('\n')
    reader = csv.DictReader(lines)
    
    extracted_data = []
    for row in reader:
        extracted_data.append(row)

    print(f"Extracted {len(extracted_data)} records.")
    
    # For simplicity, we'll pass the extracted data as a string to the next lambda
    # In a real scenario, you might store it in a temporary S3 location or a database
    return {
        'statusCode': 200,
        'body': json.dumps(extracted_data)
    }
