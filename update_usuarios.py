def lambda_handler(event, context):
    tenant_id = event['body']['tenantID']
    
    # Update last access time
    ultimo_acceso = datetime.datetime.utcnow().isoformat()
    
    response = table.update_item(
        Key={'tenantID': tenant_id},
        UpdateExpression="set ultimoAcceso = :ultimo_acceso",
        ExpressionAttributeValues={':ultimo_acceso': ultimo_acceso},
        ReturnValues="UPDATED_NEW"
    )
    
    return {
        'statusCode': 200,
        'body': response['Attributes']
    }
