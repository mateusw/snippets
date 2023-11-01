#!/usr/bin/python
#pip install google-cloud-notebooks
from google.cloud import notebooks_v1
from google.api_core import exceptions as core_exceptions
import datetime

client = notebooks_v1.NotebookServiceClient()

def restart_notebook_instance(instance_full_name: str):
    try: 
        print(datetime.datetime.now())
        operation = client.start_instance(
            {
                "name": instance_full_name
            }
        )
        print("Waiting for operation to complete...")
        response = operation.result()
        return response
    except core_exceptions.ServiceUnavailable:
        print("Unavailable, trying again...")
        return None

status = None
while(status == None):
    status = restart_notebook_instance("projects/YOU_GCP_PROJECT_NAME_HERE/locations/us-central1-a/instances/pytorch2-a100")
    print(status)



