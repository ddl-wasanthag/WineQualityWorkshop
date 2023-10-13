split = 70
max_models = 10
max_runtime_sec = 30
sort_metric ="r2"
script_name = f"scripts/dataset_write_job.py {split} {max_models} {max_runtime_sec} {sort_metric}"


import os
from domino import Domino

api_key = os.environ['SECURE_USER_API_TOKEN']
project_url = os.environ['DOMINO_PROJECT_OWNER'] + "/" + os.environ['DOMINO_PROJECT_NAME']

domino = Domino(
    project_url,        ##### CONFIG
    api_key=api_key,
    host=os.environ["DOMINO_API_HOST"],
)

domino.job_start_blocking(command=script_name)
