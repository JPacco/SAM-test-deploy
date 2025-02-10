# functions/delete.py
import json
import os
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    user_id = event['pathParameters']['id']
    
    try:
        table.delete_item(Key={'id': user_id})
        
        return {
            'statusCode': 204,
            'body': json.dumps({'message': 'User deleted successfully'})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }