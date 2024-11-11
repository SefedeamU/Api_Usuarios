def lambda_handler(event, context):
    # Extract email or tenantID from query parameters
    tenant_id = event.get('queryStringParameters', {}).get('tenantID')
    email = event.get('queryStringParameters', {}).get('email')
    
    # Query DynamoDB
    if tenant_id:
        response = table.get_item(Key={'tenantID': tenant_id})
    elif email:
        response = table.scan(FilterExpression=Attr('email').eq(email))
    else:
        return {'statusCode': 400, 'body': 'Debe proporcionar tenantID o email'}
    
    item = response.get('Item')
    
    if not item:
        return {'statusCode': 404, 'body': 'Usuario no encontrado'}
    
    # Return user data without password hash
    item.pop('passwordHash', None)
    return {
        'statusCode': 200,
        'body': item
    }
