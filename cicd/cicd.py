#!/usr/bin/env python
import argparse,os
from domino import Domino

def parse_args():
    parser=argparse.ArgumentParser(description="a script to do stuff")
    parser.add_argument("DOMINO_PROJECT_OWNER")
    parser.add_argument("DOMINO_PROJECT_NAME")
    parser.add_argument("DOMINO_USER_API_KEY")
    parser.add_argument("DOMINO_API_HOST")
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


def main():
    inputs=parse_args()
    print(inputs.DOMINO_PROJECT_OWNER)
    print(inputs.DOMINO_PROJECT_NAME)
    print(inputs.DOMINO_USER_API_KEY)
    print(inputs.DOMINO_API_HOST)

    project=  inputs.DOMINO_PROJECT_OWNER + "/" + inputs.DOMINO_PROJECT_NAME
    domino = Domino(
        project,
        api_key=inputs.DOMINO_USER_API_KEY,
        host=inputs.DOMINO_API_HOST,
    )

    list_environments(domino)

if __name__ == '__main__':
    main()
