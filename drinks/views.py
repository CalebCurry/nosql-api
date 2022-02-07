from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import boto3

@api_view(['GET', 'POST'])
def drinks(request):
    db = boto3.resource('dynamodb')
    table = db.Table('drinks')
    if request.method == 'GET':
        drinks = table.scan()
        return Response({'drinks': drinks.get('Items')})
    elif request.method == 'POST':
        try:
            table.put_item(Item=request.data)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Failed to insert'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
def drink(request, name):
    db = boto3.resource('dynamodb')
    table = db.Table('drinks')
    if request.method == 'GET':
        drink = table.get_item(Key={
            'name': name
        })

        if (drink.get('Item') is not None):
            return Response({'drink': drink.get('Item')}) 
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        try:
            table.put_item(Item=request.data)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Failed to update'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == 'DELETE':
        table.delete_item(Key={
            'name': name
        })
        return Response(status=status.HTTP_200_OK)