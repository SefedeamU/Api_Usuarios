import hashlib

def lambda_handler(event, context):
    email = event['body']['email']
    password = event['body']['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    response = table.scan(FilterExpression=Attr('email').eq(email))
    item = response.get('Items', [])
    
    if not item:
        return {'statusCode': 404, 'body': 'Usuario no encontrado'}
    
    if item[0]['passwordHash'] != password_hash:
        return {'statusCode': 401, 'body': 'Contraseña incorrecta'}
    
    # Actualiza el último acceso
    table.update_item(
        Key={'tenantID': item[0]['tenantID']},
        UpdateExpression="set ultimoAcceso = :ultimo_acceso",
        ExpressionAttributeValues={':ultimo_acceso': datetime.datetime.utcnow().isoformat()},
    )
    
    return {'statusCode': 200, 'body': 'Inicio de sesión exitoso'}
