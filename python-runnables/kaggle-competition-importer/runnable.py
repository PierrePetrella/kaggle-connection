# -*- coding: utf-8 -*-
# This file is the actual code for the Python runnable kaggle-competition-importer
from dataiku.runnables import Runnable
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import os, json, subprocess, csv
import zipfile
from kaggleconnection import utils


class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
        self.KAGGLE_CHALLENGE_URL = self.config.get('KAGGLE_CHALLENGE_URL')
        self.KAGGLE_KEY = self.config.get('KAGGLE_KEY')
        self.KAGGLE_USERNAME = self.config.get('KAGGLE_USERNAME')
        self.connection = self.config.get('connection')
        
        self.client = dataiku.api_client()
        self.project = self.client.get_default_project()
        self.challenge_ref = self.KAGGLE_CHALLENGE_URL.split("/")[-1]
        self.tmp_dir = dataiku.get_custom_variables()["dip.home"] + "/tmp/kaggle"
        self.download_folder = self.tmp_dir +"/challenge_download"
        self.leaderboard_folder = self.tmp_dir + "/leaderboard"
        self.leaderboard_zip_file = self.leaderboard_folder +"/"+ self.challenge_ref + ".zip"
        self.zip_path = self.download_folder + "/" +self.challenge_ref + ".zip"
        
        
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
       
        ### Authentication to Kaggle ### 
        os.environ["KAGGLE_KEY"] = self.KAGGLE_KEY
        os.environ["KAGGLE_USERNAME"] = self.KAGGLE_USERNAME
        import kaggle
        kaggle.api.authenticate()
        os.environ["KAGGLE_KEY"] = ""
        os.environ["KAGGLE_USERNAME"] = ""
        
        ### Check tmp folder is well formated ###
        utils.check_dir(self.tmp_dir)
        utils.check_dir(self.download_folder)
        utils.check_dir(self.leaderboard_folder)
        
        ### Import competition datasets from kaggle to the Flow ###
        kaggle.api.competition_download_files(self.challenge_ref, path=self.download_folder)
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.tmp_dir)
        
        utils.create_dataset_from_csv(self.project, self.tmp_dir, self.connection)
        utils.empty_tmp_dir(self.tmp_dir)
        
        ### Build leaderboard dataset ###
        kaggle.api.competition_leaderboard_download(self.challenge_ref, self.leaderboard_folder)

        with zipfile.ZipFile(self.leaderboard_zip_file, 'r') as zip_ref:
            zip_ref.extractall(self.tmp_dir)

        utils.create_dataset_from_csv(self.project, self.tmp_dir, self.connection)
        utils.empty_tmp_dir(self.tmp_dir)
        
        ### Build metadata dataset ###
        competition_list = kaggle.api.competitions_list(search=self.challenge_ref)
        if (len(competition_list)>0):
            competition = competition_list[0]
            ds_vars = vars(competition)
            metadata = []
            values = []
            for var in ds_vars:
                metadata.append(var)
                values.append(ds_vars[var])
            df = pd.DataFrame()
            df["metadata"] = metadata
            df["values"]= values
            dataset_name = "metadata"
            builder = self.project.new_managed_dataset(dataset_name)
            builder.with_store_into(self.connection)
            dataset = builder.create(overwrite=True)
            dataiku.Dataset(dataset_name).write_with_schema(df)
        else:
            print ("Can't extract competition metadata",competition_list)
        
        return "Kaggle competition data has been imported"
        
        
        
        
        
        
        

        
