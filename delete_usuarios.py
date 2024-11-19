import boto3
import os

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ['USERS_TABLE']
table = dynamodb.Table(USERS_TABLE)

def lambda_handler(event, context):
    tenant_id = event['body']['tenantID']
    user_id = event['body']['userID']

    response = table.delete_item(Key={'tenantID': tenant_id, 'userID': user_id})

    return {
        'statusCode': 204,
        'body': 'Usuario eliminado'
    }