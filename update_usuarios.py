import boto3
import datetime
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    tenant_id = event['body']['tenantID']
    user_id = event['body']['userID']
    nombre = event['body'].get('nombre')
    email = event['body'].get('email')

    update_expression = "set "
    expression_attribute_values = {}

    if nombre:
        update_expression += "nombre = :nombre, "
        expression_attribute_values[':nombre'] = nombre

    if email:
        update_expression += "email = :email, "
        expression_attribute_values[':email'] = email

    update_expression = update_expression.rstrip(', ')

    response = table.update_item(
        Key={'tenantID': tenant_id, 'userID': user_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="UPDATED_NEW"
    )

    return {
        'statusCode': 200,
        'body': response['Attributes']
    }