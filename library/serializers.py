from rest_framework import serializers
from .models import *


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksMaster
        fields = ['id' , 'name', 'author','price']



class InventorySerializer(serializers.ModelSerializer):
    books = serializers.CharField(source='book.name' )

    class Meta:
        model = InventoryMaster
        fields = ['id' , 'copies_available' , 'books']


class IssuesSerializer(serializers.ModelSerializer):
    book = serializers.CharField( source='issued_book.name' , read_only = True)
    class Meta:
        model = Issues
        fields = ['user' , 'book' , 'issue_date' , 'due_date' , 'due_amount'] 