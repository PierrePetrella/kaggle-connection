# HOW TO USE THIS KAGGLE PLUGIN 

This plugin is composed of two components (macros):
- a kaggle competition data importer
- a kaggle competition submission tool


# Python environemt

You will require to install a python environement with this plugin.
The only package required is the kaggle API:
``` kaggle ```


# Setup:

1. Connect to the [kaggle website](https://www.kaggle.com/)
2. Generate a API key
- Account > API > Create New API Token
- extract your *username* and *key* for the *kaggle.json* file
3. Install the plugin *(ADD PLUGIN > Fetch from Git repository)*
- Repository url : https://github.com/PierrePetrella/kaggle-connection.git
- Checkout : ```master``` or ```x.y.z``` branch
- Path in repository : leave empty or ```/```
4. Intall the required python environment *(PYTHON37)*
5. Execute the macro : ```kaggle-competition-importer```
- You can execute it in:
	- In the macro settings of the project
	- As a step in a scenario
- **You will need to register for the given competition before hand**
6. Build your flow and a create an output dataset in the same format as the sample dataset.
7. To submit the dataset run : ```kaggle-competition-submit```
- You can execute it in:
	- In the macro settings of the project
	- As a step in a scenario

# How to test the plugin

There are no tests for this plugin. You will have to trust me..