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
        
        self.SUBMISSION_DESC = self.config.get('SUBMISSION_DESC')
        self.SUBMISSION_FILE_NAME = self.config.get('SUBMISSION_FILE_NAME')
        self.SUBMISSION_DATASET = self.config.get('SUBMISSION_DATASET')
        self.KAGGLE_CHALLENGE_URL = self.config.get('KAGGLE_CHALLENGE_URL')
        self.KAGGLE_KEY = self.config.get('KAGGLE_KEY')
        self.KAGGLE_USERNAME = self.config.get('KAGGLE_USERNAME')
        self.connection = self.config.get('connection')
        
        self.client = dataiku.api_client()
        self.project = self.client.get_default_project()
        self.challenge_ref = self.KAGGLE_CHALLENGE_URL.split("/")[-1]
        self.tmp_dir = dataiku.get_custom_variables()["dip.home"] + "/tmp/kaggle"
        self.submission_file_path = self.tmp_dir + "/" + self.SUBMISSION_FILE_NAME
        
        
        
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
        
        ### Read DSS dataset for submission ###
        submission = dataiku.Dataset(self.SUBMISSION_DATASET)
        df_submission = submission.get_dataframe()
        
        # Write tmp submission csv
        df_submission.to_csv(self.submission_file_path, index=False)
        # Submit CSV to kaggle
        kaggle.api.competition_submit(self.submission_file_path, self.SUBMISSION_DESC, self.challenge_ref)

        ### Disconnect from kaggle + clean up ###
        utils.empty_tmp_dir(self.tmp_dir)
        
        return "Kaggle competition data has been imported"