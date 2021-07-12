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


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = InventoryMaster.objects.all()
    serializer_class = InventorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('book__name',)


class IssuesViewSet(viewsets.ModelViewSet):
    queryset = InventoryMaster.objects.all()
    serializer_class = InventorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user','book__name')



@csrf_exempt
def issue_book(request):
    """
    Logic for fetching the issues of a particular user and giving the amount to be paid and also issuing a new book.
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
                """This is to minus the copies available by 1 once the book is issued """
                inventory.copies_available -= 1
                inventory.save()
                return JsonResponse({"message" : "Book Issued"}, status=201)
            except Exception as e:
                return JsonResponse({"message" : "Unable to Process Request"}, status=400)
    try:
        user = request.GET.get('user' , None)
        issues = Issues.objects.get(user=user)
        if request.method == 'GET':
            date_format = "%m/%d/%Y"
            current_date =  datetime.today()
            due_date = issues.due_date
            delta = current_date - due_date
            extra_days = delta.days
            if extra_days > 0:
                issues.due_amount += (extra_days*10)
                issues.save()
            serializer = IssuesSerializer(issues)
            return JsonResponse(serializer.data, safe=False , status = 200)
        
        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            data['due_date'] = datetime.now()+timedelta(days=7)
            serializer = IssuesSerializer(issues, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
    except Issues.DoesNotExist:
        return JsonResponse({"User Not found" : []}, status=200)
        