import boto3
import hashlib
import datetime
import os
import json
import jwt
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ['USERS_TABLE']
table = dynamodb.Table(USERS_TABLE)
JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGORITHM = 'HS256'

def lambda_handler(event, context):
    try:
        # Parse the event body
        body = json.loads(event['body'])
        email = body['email']
        password = body['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        response = table.scan(FilterExpression=Attr('email').eq(email))
        items = response.get('Items', [])

        if not items:
            return {'statusCode': 404, 'body': 'Usuario no encontrado'}

        item = items[0]
        if item['passwordHash'] != password_hash:
            return {'statusCode': 401, 'body': 'Contraseña incorrecta'}

        ultimo_acceso = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        table.update_item(
            Key={'tenantID': item['tenantID'], 'userID': item['userID']},
            UpdateExpression="set ultimoAcceso = :ultimo_acceso",
            ExpressionAttributeValues={':ultimo_acceso': ultimo_acceso},
        )

        # Generate JWT token
        payload = {
            'tenantID': item['tenantID'],
            'userID': item['userID'],
            'email': item['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Inicio de sesión exitoso', 'token': token})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }