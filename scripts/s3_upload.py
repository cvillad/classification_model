#!/usr/bin/env python

import boto3
import argparse
import tarfile
import os

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return output_filename

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src','-s', type=str, required=True, help='folder source')
    parser.add_argument('--bucket','-b', type=str, default='sagemaker-us-west-2-430127992102', help='bucket name')
    parser.add_argument('--key','-k', type=str, default='ClassificationModel', help='key name')
    parser.add_argument('--datadir','-d', type=str, default='dataset', help='directory name')
    parser.add_argument('--object','-o', type=str, default='dataset.tar.gz', help='object name') #name_file in s3 bucket
    opt = parser.parse_args()
    
    source_name = opt.src
    bucket_name = opt.bucket
    bucket_key = opt.key
    bucket_dir = opt.datadir
    object_name = opt.object
    
    s3 = boto3.resource('s3')
    
    if os.path.isfile(source_name):
        s3.Bucket(bucket_name).upload_file(source_name, os.path.join(bucket_key, bucket_dir, object_name))
        
    else:
        output_filename = make_tarfile(os.path.join(os.getcwd(),object_name), source_name)
        s3.Bucket(bucket_name).upload_file(output_filename, os.path.join(bucket_key, bucket_dir, object_name))
        os.remove(output_filename)