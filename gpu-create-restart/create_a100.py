#!/usr/bin/python
#pip install google-cloud-notebooks
from google.cloud import notebooks_v1
from google.api_core import exceptions as core_exceptions
import datetime

client = notebooks_v1.NotebookServiceClient()

request = {
    'parent': 'projects/YOU_GCP_PROJECT_NAME_HERE/locations/us-central1-a',
    'instance_id': 'pytorch2-a100',
    'instance': {
        'install_gpu_driver': True,
        'machine_type': 'a2-highgpu-1g',
        'vm_image': {
            'image_name': "pytorch-2-0-gpu-notebooks-v20230925-debian-11-py310",
            'project': "deeplearning-platform-release"
        }
    }
}

def create_notebook_instance(request):
    try: 
        print(datetime.datetime.now())
        operation = client.create_instance(request=request)
        print("Waiting for operation to complete...")
        response = operation.result()
        return response
    except core_exceptions.ServiceUnavailable:
        print("Unavailable, trying again...")
        return None

status = None
while(status == None):
    status = create_notebook_instance(request)
    print(status)




