from django.http import HttpResponse, JsonResponse
from datetime import datetime
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django_filters import rest_framework as filters
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from .models import *




class BooksViewSet(viewsets.ModelViewSet):
    queryset = BooksMaster.objects.all()
    serializer_class = BooksSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name','author')

    def create(self, request):
        try: 
            post_data =request.data
            BooksMaster.objects.create(**post_data)
            return JsonResponse({"message" : "New Book Added"} ,  status=200)
        except Exception as e:
            return JsonResponse({"message" : "Error while adding a book"} ,  status=400)

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = InventoryMaster.objects.all()
    serializer_class = InventorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('book__name',)

    def create(self, request):
        try: 
            post_data =request.data
            book = BooksMaster.objects.get(id=post_data['book'])
            post_data['book']=book
            InventoryMaster.objects.create(**post_data)
            return JsonResponse({"message" : "Stock Added"} ,  status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"message" : "Error while adding"} ,  status=400)



class IssuesViewSet(viewsets.ModelViewSet):
    queryset = InventoryMaster.objects.all()
    serializer_class = InventorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user','book__name')



@csrf_exempt
def issue_book(request):
    """
    Logic for fetching the issues of a particular user and giving the amount to be paid and also issuing a new book.

    Also the logic for updating the books and reissuing for a particular user
    """
   
    if request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            issues = Issues.objects.get(user=data['user'])
            return JsonResponse({"message" : "Book already Issued"}, status=400)
        except Issues.DoesNotExist:
            book = BooksMaster.objects.get(id = data['issued_book'])
            data['issued_book'] = book
            print('Data is' , data)
            data['due_amount'] = book.price
            try:
                Issues.objects.create(**data)
                inventory = InventoryMaster.objects.get(book__id=book.id)

                """This is to minus the copies available by 1 , once the book is issued """
                inventory.copies_available -= 1
                inventory.save()

                return JsonResponse({"message" : "Book Issued"}, status=201)
            except Exception as e:
                return JsonResponse({"message" : "Unable to Process Request"}, status=400)

    if request.method == 'GET':
        try:
            user = request.GET.get('user' , None)
            issues = Issues.objects.get(user=user)
            date_format = "%m/%d/%Y"
            current_date =  datetime.today()
            due_date = issues.due_date
            delta = current_date - due_date
            extra_days = delta.days
            if extra_days > 0:
                issues.due_amount += (extra_days*10) #Updates the due amount for the user at the time of returning
                issues.save()
            serializer = IssuesSerializer(issues)
            return JsonResponse(serializer.data, safe=False , status = 200)
        except Issues.DoesNotExist:
            return JsonResponse({"User Not found" : []}, status=200)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        try:
            book = BooksMaster.objects.get(id = data['issued_book'])
            inventory = InventoryMaster.objects.get(book__id=data['issued_book'])
            issues = Issues.objects.get(user=data['user'])

            """Condition to return the book and delete the records"""
            if data['return']:
                inventory.copies_available += 1 #Updates the Inventory of the returned book
                inventory.save()
                Issues.objects.filter(user = data['user']).delete()
                return JsonResponse({"message" : "Book returned" }, status=200)

            """Condition to reissue the same book"""
            if data['reissue'] and issues.issued_book_id == book.id:
                data['due_date'] = datetime.now()+timedelta(days=7) #The due date is updated with 7 days from date of issue
                serializer = IssuesSerializer(issues, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors, status=400)

            """Condition to issue a new book to the person"""
            if data['reissue']:
                Issues.objects.filter(user=data['user']).update(issued_book=book , due_amount=book.price , due_date=datetime.now()+timedelta(days=7))
                inventory.copies_available -= 1 #Updates the inventory of the new book issued
                inventory.save()
                return JsonResponse({"message":"New Book Issued"} , status=200)
           
        except BooksMaster.DoesNotExist:
            return JsonResponse({"message" : "Unable to process the request"}, status=400)
            
        