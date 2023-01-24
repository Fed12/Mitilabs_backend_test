from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
import streamlit as st
import pandas as pd
from myapp.visualize import load_data, sidebar_filter, plot
import boto3
from .settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
import requests
from .serializers import FileSerializer


def get_single_file_from_bucket(file_name):
    client = boto3.resource('s3',
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name='eu-south-1', endpoint_url='https://s3.eu-south-1.amazonaws.com'
                            )
    my_bucket = client.Bucket(AWS_STORAGE_BUCKET_NAME)
    return my_bucket.objects.filter(Prefix='s3://' + AWS_STORAGE_BUCKET_NAME + '/' + first_file_name)

def load_data(first_file_name):

    if not file_name:
          print("No filename specified")

    s3_resource = boto3.resource('s3')
    first_bucket = s3_resource.Bucket(AWS_STORAGE_BUCKET_NAME)

    # Send bucket name and file name in request body
    bucket_name = request.data.get('bucket_name')
    file_name = request.data.get('file_name')
    # bucket_name = 'havtrackwatchappmain42b95d92f7eb4d85aa3b21a88ae125522-dev'
    # file_name = 'Cachedtest_file_(1).xls'

    first_object = s3_resource.Object(bucket_name=AWS_STORAGE_BUCKET_NAME, key=file_name)

    file = get_single_file_from_bucket(file_name)

    client = boto3.resource('s3',
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name='eu-south-1', endpoint_url='https://s3.eu-south-1.amazonaws.com'
                            )

    first_bucket_name = s3_resource.Bucket(AWS_STORAGE_BUCKET_NAME)
    # first_bucket_name = 'havtrackwatchappmain42b95d92f7eb4d85aa3b21a88ae125522-dev'
    first_file_name = 'Cachedtest_file_(1).xls'
    first_object = s3_resource.Object(bucket_name=AWS_STORAGE_BUCKET_NAME, key=first_file_name)

    print(' type(first_object)')
    print(type(first_object), ' type(first_object)')
    print(' type(first_object)')

    data = pd.read_excel('s3://' + first_bucket_name + '/' + first_file_name)
    df = pd.read_excel(first_object, engine='xlrd')
    df = df.rename(columns={'Motion Sensor': 'date', 'Unnamed: 1': "sensor"})
    df = df.drop(columns={'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'})
    # lowercase = lambda x: str(x).lower()
    # df.rename(lowercase, axis='columns', inplace=True)

    import datetime as dt
    df['date'] = pd.to_datetime(df['date'])
    df['YW'] = df['date'].dt.year * 100 + df['date'].dt.isocalendar().week
    df['date'] = pd.to_datetime(df['date'])
    df = df.dropna()

    return df

from .serializers import FileUploadSerializer
from .helpers import *


class FileUpload(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser, JSONParser)
    renderer_classes = (JSONRenderer,)
	
    def post(self, request):

        file = request.FILES.get('file')
        # collection_name = request.query_params.get('collection_name')
        # force = request.query_params.get('force')
        # data = json.load(svjl_file)
        # upload_check = mongo_upload_check(collection_name, data)
        
        # if upload_check:
        #     return Response({"status": upload_check}, status=400)

        db = get_database(MONGO_DB, collection_name)
        
        originalNrrdMd5 = data['originalNrrdMd5']

        bucket_name = AWS_STORAGE_BUCKET_NAME
        duplicate = list(db.find({"originalNrrdMd5": originalNrrdMd5}))

        if duplicate:
            return Response('already exists', status=400)

        id = str(db.insert_one(data).inserted_id)
        new_svjl = SVLJFile(mongo_key=id, vlj_data=data, )
        file = ContentFile(image_64_decode)
        new_svjl.file_bin.save(f'volume_{hash_object.hexdigest()}.vl', file)
        new_svjl.save()
        new_file = get_single_file_from_bucket(f'volume_{hash_object.hexdigest()}.vl')
        new_file = list(new_file)[0]
        db.update_one({"_id": ObjectId(id)}, {"$set": {"etag": new_file.e_tag.replace('"', "")}})

        return Response({'key': id}, status=201)




class Visualize(GenericAPIView):
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        """
        No parameters
        """ 

        


        # print(request.headers, ' request.headers')

        # files = my_bucket.objects.filter(
        #     Prefix=f's3://havtrackwatchappmain42b95d92f7eb4d85aa3b21a88ae125522-dev/public//storage/emulated/0/Android/data/'
        #            f'com.example.hav_track/files/')
        # print(files, ' files')


        # df = load_data(file_name)
        # sidebar_filter(df)
        # plot(df)
        # print(df.date)

        # TITLES
        # st.title("Cached data")
        # st.sidebar.title("Sidebar Slider Filter")

        response={}
        return Response(response, status=200) 