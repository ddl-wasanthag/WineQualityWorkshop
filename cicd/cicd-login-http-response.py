#!/usr/bin/env python
import argparse,os
from domino import Domino

def parse_args():
    parser=argparse.ArgumentParser(description="a script to publish Domino Models")
    parser.add_argument("DOMINO_MODEL_OP", type=str, help="create, list or update.")
    parser.add_argument("DOMINO_PROJECT_OWNER", type=str, help="Domino Project Owner.")
    parser.add_argument("DOMINO_PROJECT_NAME", type=str, help="Domino Project Name.")
    parser.add_argument("DOMINO_USER_API_KEY", type=str, help="Domino user API Key.")
    parser.add_argument("DOMINO_API_HOST", type=str, help="Domino URL for external or http://nucleus-frontend.domino-platform:80 from a workspace.")
    parser.add_argument("DOMINO_MODEL_NAME", type=str, help="Name of the model.")
    parser.add_argument("DOMINO_MODEL_DESC", type=str, help="Description of the model.")
    parser.add_argument("DOMINO_MODEL_FILE", type=str, help="Name of the model file.")
    parser.add_argument("DOMINO_MODEL_FUNC", type=str, help="Name of the model function.")
    parser.add_argument("DOMINO_MODEL_CE", type=str, help="ID of the model compute environment.")
    parser.add_argument("DOMINO_MODEL_LOG_HTTP_RR", type=str, help="ID of the model compute environment.")
    args=parser.parse_args()
    return args

def list_environments(domino):
    all_available_environments = domino.environments_list()
    global_environments = list(
        filter(
            lambda x: x.get("visibility") == "Global", all_available_environments["data"]
        )
    )
    print(
        "This Domino deployment has \
         {} global environments".format(
            len(global_environments)
        )
    )
    
def list_models(domino):
    print(f"{domino.models_list()}")
    
def model_exist(domino, model_name):
    models = domino.models_list()
    for i in models['data']:
        if i['name'] == model_name:
            return True     

def create_model(domino,model_name, model_desc, model_file, model_func, model_ce, model_loghttprr):
    # Publish a brand new model
    published_model = domino.model_publish(
    file=model_file,
    function=model_func,
    environment_id=model_ce,
    name=model_name,
    description=model_desc,
    logHttpRequestResponse=model_loghttprr,
    )
    published_model_id = published_model.get("data", {}).get("_id")
    print("Model {} published, details below:".format(published_model_id))
    print(published_model)

    
def publish_revision(domino,model_name, model_desc, model_file, model_func, model_ce, model_loghttprr):
    # Publlish another version for this model
    models = domino.models_list()
    for i in models['data']:
        if i['name'] == model_name:
            published_model_id = i['id']      
    another_model_version = domino.model_version_publish(
    model_id=published_model_id,
    file=model_file,
    function=model_func,
    environment_id=model_ce,
    description=model_desc,
    logHttpRequestResponse=model_loghttprr,
    )
    
def main():
    inputs=parse_args()
    print(inputs.DOMINO_MODEL_NAME)
    #print(inputs.DOMINO_PROJECT_NAME)
    #print(inputs.DOMINO_USER_API_KEY)
    #print(inputs.DOMINO_API_HOST)

    project=  inputs.DOMINO_PROJECT_OWNER + "/" + inputs.DOMINO_PROJECT_NAME
    domino = Domino(
        project,
        api_key=inputs.DOMINO_USER_API_KEY,
        host=inputs.DOMINO_API_HOST,
    )
    if inputs.DOMINO_MODEL_OP == "list":
        list_models(domino)
    elif inputs.DOMINO_MODEL_OP == "create":
        create_model(domino,inputs.DOMINO_MODEL_NAME, inputs.DOMINO_MODEL_DESC, inputs.DOMINO_MODEL_FILE, inputs.DOMINO_MODEL_FUNC, inputs.DOMINO_MODEL_CE, inputs.DOMINO_MODEL_LOG_HTTP_RR)
    elif inputs.DOMINO_MODEL_OP == "update":
        publish_revision(domino,inputs.DOMINO_MODEL_NAME, inputs.DOMINO_MODEL_DESC, inputs.DOMINO_MODEL_FILE, inputs.DOMINO_MODEL_FUNC, inputs.DOMINO_MODEL_CE, inputs.DOMINO_MODEL_LOG_HTTP_RR) 
    elif inputs.DOMINO_MODEL_OP == "publish":    
        if model_exist(domino, inputs.DOMINO_MODEL_NAME):
            publish_revision(domino,inputs.DOMINO_MODEL_NAME, inputs.DOMINO_MODEL_DESC, inputs.DOMINO_MODEL_FILE, inputs.DOMINO_MODEL_FUNC, inputs.DOMINO_MODEL_CE, inputs.DOMINO_MODEL_LOG_HTTP_RR)
        else :
            create_model(domino,inputs.DOMINO_MODEL_NAME, inputs.DOMINO_MODEL_DESC, inputs.DOMINO_MODEL_FILE, inputs.DOMINO_MODEL_FUNC, inputs.DOMINO_MODEL_CE)
        
        

if __name__ == '__main__':
    main()

