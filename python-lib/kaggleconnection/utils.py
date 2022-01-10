# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import os, json, subprocess, csv
import zipfile

###############################################################
# Collect all the csv files at the root of the tmp_dir and turn 
# them into DSS Datasets in the flow
# INPUT : project, tmp_dir, connection
# OUTPUT : null (This function is a procedure)

###############################################################
def create_dataset_from_csv(project, tmp_dir, connection):
    dirs = os.listdir(tmp_dir)  
    for file in dirs:
        if file.endswith('.csv'):
            df = pd.read_csv(tmp_dir +"/"+ file)
            file_name = file[:-4]
            if file_name in [p["name"] for p in project.list_datasets()]:
                print ("dataset already created")
            else:
                builder = project.new_managed_dataset(file_name)
                builder.with_store_into(connection)
                dataset = builder.create(overwrite=True)
                dataiku.Dataset(file_name).write_with_schema(df)

            

###############################################################
# Procedure used to remove any csv written in the tmp file root
# INPUT : tmp_dir
# OUTPUT : null (This function is a procedure)

###############################################################
def empty_tmp_dir(tmp_dir):
    dirs = os.listdir(tmp_dir)
    for file in dirs:
        if file.endswith('.csv'):
            os.remove(tmp_dir + "/"+ file)
            print (file + " successfully removed")
            
            
            
###############################################################
# Check that the directory exists, if no, build it
# INPUT : tmp_dir
# OUTPUT : null (This function is a procedure)

###############################################################
def check_dir(tmp_dir):
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)