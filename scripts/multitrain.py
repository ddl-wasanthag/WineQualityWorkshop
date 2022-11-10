import domino
import os
import time

print('Initializing Domino Project for API calls')

#initialize Domino Project
domino_project =domino.Domino(project = str(os.environ.get('DOMINO_PROJECT_OWNER')+'/'+os.environ.get('DOMINO_PROJECT_NAME')),
                              api_key = os.environ.get('DOMINO_USER_API_KEY'),
                              domino_token_file=os.environ.get('DOMINO_TOKEN_FILE'))


print('Kicking off sklearn model training')
domino_project.job_start(command='scripts/sklearn_model_train.py')

print('Kicking off R model training')
domino_project.job_start(command='scripts/R_model_train.R')


print('Kicking off h2o model training')
domino_project.job_start(command='scripts/h2o_model_train.py')

print('Done!')