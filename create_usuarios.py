import boto3
import uuid
import datetime
import hashlib
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    tenant_id = event['body']['tenantID']
    email = event['body']['email']
    nombre = event['body']['nombre']
    password = event['body']['password']

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    year_prefix = datetime.datetime.utcnow().strftime('%Y')
    user_id = str(uuid.uuid4())
    user_id = f"{year_prefix}-{user_id}"

    fecha_creacion = datetime.datetime.utcnow().strftime('%m-%dT%H:%M:%S')

    usuario = {
        'tenantID': tenant_id,
        'userID': user_id,
        'fechaCreacion': fecha_creacion,
        'nombre': nombre,
        'email': email,
        'passwordHash': password_hash,
        'ultimoAcceso': fecha_creacion
    }

    response = table.put_item(Item=usuario)

    return {
        'statusCode': 201,
        'body': {
            'message': 'Usuario creado',
            'tenantID': tenant_id,
            'userID': user_id,
            'fechaCreacion': fecha_creacion
        }
    }