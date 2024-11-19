import boto3
import hashlib
import datetime
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ['USERS_TABLE']
table = dynamodb.Table(USERS_TABLE)

def lambda_handler(event, context):
    email = event['body']['email']
    password = event['body']['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    response = table.scan(FilterExpression=Attr('email').eq(email))
    items = response.get('Items', [])

    if not items:
        return {'statusCode': 404, 'body': 'Usuario no encontrado'}

    item = items[0]
    if item['passwordHash'] != password_hash:
        return {'statusCode': 401, 'body': 'Contraseña incorrecta'}

    ultimo_acceso = datetime.datetime.utcnow().strftime('%m-%dT%H:%M:%S')
    table.update_item(
        Key={'tenantID': item['tenantID'], 'userID': item['userID']},
        UpdateExpression="set ultimoAcceso = :ultimo_acceso",
        ExpressionAttributeValues={':ultimo_acceso': ultimo_acceso},
    )

    return {'statusCode': 200, 'body': 'Inicio de sesión exitoso'}