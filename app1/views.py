from django.shortcuts import render, redirect
from .models import *
# from _thread import *
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch
import json
# from .tasks import create_db
from celery  import shared_task
import pandas as pd
from django.db import transaction
from .models import *
from datetime import datetime

# from Project1.celery import add


Elastic_username = 'elastic'
Elastic_password = 'pS+pLhxF_S8YOkU6F-UD'
hosts = "http://localhost:9200"

@shared_task()
def create_db(file_path):
    try:
        # with transaction.atomic():
            df = pd.read_csv(file_path)
            df = df.dropna(how='all')
            print(df.values)
            list_of_csv = [list(row) for row in df.values]

            for row in list_of_csv:
                Employee.objects.create(
                    emp_id = row[0],
                    name = row[1],
                    email = row[2],
                    mobile = row[3],
                    date_of_join= datetime.strptime(row[4], '%d-%b-%y').date()
                )
    except Exception as e:
        print(f"Error during database creation: {e}")
        FileError.objects.create(file_error = e.args[0])

def handle_uploaded_file(uploaded_file):
    # Assuming you have a media directory in your project to store uploaded files
    file_path = f'files/{uploaded_file.name}'

    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return file_path

def main(request):
    error_message  =''
    try:
        if request.method=="POST":
            file = request.FILES['files']
            obj = File.objects.create(file=file)
            file_path = handle_uploaded_file(file)
            # create_db(obj.file)
            print('obj.file',file_path)
            create_db.delay(file_path)
            # add.delay(1,2)
            # create_db.delay(obj.file)
            # messages.success(request, 'File uploaded successfully!')
            index_to_elasticsearch()  # Index data into Elasticsearch
            error_message = 'File uploaded successfully!'
        return render(request,"upload.html",{'error_message': error_message,})
    except Exception as e:
        print('heloooooooo',e)
        FileError.objects.create(file_error = e.args[0])
        # error_message = 'File uploaded unsuccessfully!, please check file added'
        # messages.error(request, 'File uploaded unsuccessfully!, please check file added')
        return render(request,"upload.html",{'error_message': error_message})


def create_index(es, index_name):
    # if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name,ignore=400)

def index_to_elasticsearch():
    # es = Elasticsearch([{'host': 'localhost', 'port': 9200,"scheme": "http"}])
    es = Elasticsearch(
    hosts,
    basic_auth=(Elastic_username, Elastic_password),
    # verify_certs=False
)
    index_name = 'employees'
    
    # Create index if it doesn't exist
    create_index(es, index_name)
    
    # Query data from Django database
    employees = Employee.objects.all()
    
    # Prepare data for indexing
    data = []
    for employee in employees:
        data.append({
            'emp_id': employee.emp_id,
            'name': employee.name,
            'email': employee.email,
            'mobile': employee.mobile
        })
    
    # Index data into Elasticsearch
    for entry in data:
        es.index(index=index_name, body=entry)


############-----Search Employee using number from elasticsearch------##############
def search_result(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        if mobile_number.isdigit() and len(mobile_number) == 10:
            # Initialize Elasticsearch client
            # es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200,'scheme':"http"}])
            es = Elasticsearch(
                hosts,
                basic_auth=(Elastic_username, Elastic_password),
                # verify_certs=False
            )
            index_name = 'employees'
            
            # Define the search query
            search_query = {
                "query": {
                    "match": {
                        "mobile": mobile_number
                    }
                }
            }
            
            # Execute the search query
            search_results = es.search(index=index_name, body=search_query)
            
            # Extract employee details from search results
            employees = []
            # print(search_results)
            for hit in search_results['hits']['hits']:
                # print(hit)
                employee = hit['_source']
                employees.append(employee)
            
            # Pass the search results to the template
            return render(request, 'search_result.html', {'employees': employees})
        else:
            error_message = "Please enter a valid 10-digit mobile number."
            return render(request, 'search_result.html', {'error_message': error_message})
    return render(request, 'search_result.html')
