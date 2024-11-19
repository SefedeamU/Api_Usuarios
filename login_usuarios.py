import boto3
import hashlib
import uuid
from datetime import datetime, timedelta
import json
from boto3.dynamodb.conditions import Attr

# Hashear contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    # Parse the event body
    body = json.loads(event['body'])
    email = body['email']
    password = body['password']
    hashed_password = hash_password(password)

    # Proceso
    dynamodb = boto3.resource('dynamodb')
    users_table = dynamodb.Table(os.environ['USERS_TABLE'])
    tokens_table = dynamodb.Table('t_tokens_acceso')

    response = users_table.scan(FilterExpression=Attr('email').eq(email))
    items = response.get('Items', [])

    if not items:
        return {
            'statusCode': 403,
            'body': 'Usuario no existe'
        }

    item = items[0]
    if hashed_password == item['passwordHash']:
        # Genera token
        token = str(uuid.uuid4())
        fecha_hora_exp = datetime.now() + timedelta(minutes=60)
        registro = {
            'token': token,
            'expires': fecha_hora_exp.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': item['userID']
        }
        tokens_table.put_item(Item=registro)
    else:
        return {
            'statusCode': 403,
            'body': 'Password incorrecto'
        }

    # Salida (json)
    return {
        'statusCode': 200,
        'token': token
    }