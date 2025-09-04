
# Author: Shubhk
import json

def handler(event, context):
    # The body from the previous lambda is a JSON string of the extracted data
    extracted_data = json.loads(event['body'])

    print(f"Transforming {len(extracted_data)} records.")

    transformed_data = []
    for record in extracted_data:
        try:
            record['value'] = int(record['value'])
            transformed_data.append(record)
        except (ValueError, KeyError) as e:
            print(f"Skipping record due to transformation error: {record} - {e}")

    print(f"Transformed {len(transformed_data)} records.")

    return {
        'statusCode': 200,
        'body': json.dumps(transformed_data)
    }
