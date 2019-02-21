import csv
import os

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import View
from django.shortcuts import render
import json
from django.http import JsonResponse
import pandas as pd


from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import time 
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def upload_csv_file(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        file_csv = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(file_csv.name, file_csv)
        print (filename)
        if filename.endswith('.csv'):
            request.session["csv_file_name"] = filename
            data={
                'is_csv':'yes'
            }
            return render(request, 'index.html',data)
            
        else:
            messages.error(request, 'File is not CSV type')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def csv_upload(request):
    if request.method == 'POST':
        csv_file_name = str(request.session["csv_file_name"])
        response_data ={}
        df = pd.read_csv('media/'+csv_file_name, header=None)
        Num_cols = len (df.columns)
        print (Num_cols)
        input_val =request.POST['input']
        output_val =request.POST['output']
        inp_out_sum = int(input_val)+int(output_val)
        lines =[]
        col = []
        col_x = []
        col_y =[]
        for inp in range(1,int(input_val)+1):
            col.append('x'+str(inp))
            col_x.append('x'+str(inp))
        for out in range(1,int(output_val)+1):
            col.append('y'+str(out))
            col_y.append('y'+str(out))
        if (inp_out_sum == Num_cols):
            df.loc[-1] = col
            df.index = df.index+1
            df = df.sort_index()
            new_headre = df.iloc[0]
            df = df[1:]
            df.columns = new_headre
            htmTable  =df.to_html()
            response_data = {
                'col':col,
                'col_x':col_x,
                'col_y':col_y,
                'lines':htmTable
            }
            return JsonResponse(response_data)

        else:
            response = JsonResponse({"error": "Sum of Input and output are not equat to row's length.Please try with different value"})
            response.status_code = 403 # To announce that the user isn't allowed to publish
            return response

                

    else:
        pass
    return render(request, 'index.html')
    


