from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings as conf_settings
import boto3
import logging
from  . models import Document
from  aws.forms import DocumentForm
from botocore.exceptions import ClientError
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import S3_inputbucket, S3_mainbucket, S3_updatebucket
import pandas as pd
import numpy as np
import re
import botocore
import json
#-------------------------------------------------------------------
s3 = boto3.client('s3')
s3_bucket =conf_settings.SESSION.resource('s3')



def home(request):
	return render(request, 'aws/index.html')

@login_required    
def s3_upload(request):
    if request.user.is_authenticated:
        current_user = request.user
        # getting current user id - int
        user_id =current_user.id
        print(user_id)
        username = current_user.username
        print(username)
        # getting associated bucket starts here ---
        s3name = S3_inputbucket.objects.get(bucket_belonging_to=user_id)
        #result_2 = f'"{my_str}"'
        print(s3name)# printing out: outputuser3
        #bucket_name=f'"{s3name}"'
        if conf_settings.AWS_STORAGE_BUCKET_NAME is None:
            conf_settings.AWS_STORAGE_BUCKET_NAME =str(s3name)

        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = DocumentForm()
        return render(request, 'aws/upload.html', {'form': form})


def get_s3_keys(bucket):
    keys = []
    resp = s3.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys

@login_required    
def s3file_reader(request):
    context={}

    if request.user.is_authenticated:
        current_user = request.user
        # getting current user id - int
        user_id =current_user.id
        print(user_id)
        username = current_user.username
        print(username)
        # getting associated bucket should start here ---
        s3name = S3_mainbucket.objects.get(bucket_belonging_to=user_id)
        s3bucket = S3_updatebucket.objects.get(bucket_belonging_to=user_id)
        print(s3name)
       
        is_base_key = get_s3_keys(str(s3name))
        print(is_base_key)
        
        is_update_key = get_s3_keys(str(s3bucket))
        print(s3bucket)
        #----------------------------------------------------
        bracketed_key = str(is_base_key)
		# calling Python sub() function from the re module.
        unbracketed_key = re.sub(r"[\[\]]",'',bracketed_key)
        print(unbracketed_key)
        key = unbracketed_key
        x = key
        rq_key = ""
        for i in x:
            if(i not in "'"):
                rq_key = rq_key + i
                print(rq_key)
        #----------------------------------------------------
        brkt_updkey = str(is_update_key)
        # calling Python sub() function from the re module.
        unbrkt_updkey = re.sub(r"[\[\]]",'',brkt_updkey)
        print(unbrkt_updkey)
        updatekey = unbrkt_updkey
        y = updatekey
        rq_updatekey = ""
        for j in y:
            if(j not in "'"):
                rq_updatekey = rq_updatekey + i
                print(rq_updatekey)

        base_obj = s3_bucket.Object(str(s3name), rq_key)
        update_obj = s3_bucket.Object(str(s3bucket), rq_updatekey)
        #Reading the File as String With Encoding
        base_content = base_obj.get()['Body'].read().decode('utf-8')
        update_content = update_obj.get()['Body'].read().decode('utf-8')
        json_base = json.loads(base_content)
        json_update = json.loads(update_content)

        df_base = pd.json_normalize(json_base)
        df_update = pd.json_normalize(json_update)
        #To perform comparasion, calculation logic based on df_base & df_update
        print("Dataframe difference -- \n")
        df = df_base.compare(df_update)
        output_html = df.to_html()
        return HttpResponse(output_html)
