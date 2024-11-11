def lambda_handler(event, context):
    tenant_id = event['body']['tenantID']
    
    response = table.delete_item(Key={'tenantID': tenant_id})
    
    return {
        'statusCode': 204,
        'body': 'Usuario eliminado'
    }
