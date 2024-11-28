import boto3
import os
import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ['USERS_TABLE']
table = dynamodb.Table(USERS_TABLE)

def lambda_handler(event, context):
    try:
        # Log the received event
        logger.info("Received event: %s", json.dumps(event))

        last_evaluated_key = event.get('queryStringParameters', {}).get('lastEvaluatedKey')
        limit = int(event.get('queryStringParameters', {}).get('limit', 10))
        scan_params = {
            'Limit': limit,
        }

        if last_evaluated_key:
            scan_params['ExclusiveStartKey'] = json.loads(last_evaluated_key)

        response = table.scan(**scan_params)

        items = response.get('Items', [])
        last_evaluated_key = response.get('LastEvaluatedKey', None)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'usuarios': items,
                'lastEvaluatedKey': json.dumps(last_evaluated_key) if last_evaluated_key else None
            })
        }
    except Exception as e:
        logger.error("Error fetching users: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }