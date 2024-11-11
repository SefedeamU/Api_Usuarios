import boto3
import uuid
import datetime
import hashlib
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Extract information from event
    email = event['body']['email']
    nombre = event['body']['nombre']
    password = event['body']['password']
    
    # Hash the password (consider using a stronger hashing library for production)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Generate tenantID with date and unique user ID
    date_prefix = datetime.datetime.utcnow().strftime('%Y%m')
    user_id = str(uuid.uuid4())
    tenant_id = f"{date_prefix}-{user_id}"
    
    # Get current timestamp for creation
    fecha_creacion = datetime.datetime.utcnow().isoformat()
    
    # Create item
    usuario = {
        'tenantID': tenant_id,
        'fechaCreacion': fecha_creacion,
        'nombre': nombre,
        'email': email,
        'passwordHash': password_hash,
        'ultimoAcceso': fecha_creacion
    }
    
    # Save item to DynamoDB
    response = table.put_item(Item=usuario)
    
    return {
        'statusCode': 201,
        'body': {
            'message': 'Usuario creado',
            'tenantID': tenant_id,
            'fechaCreacion': fecha_creacion
        }
    }
