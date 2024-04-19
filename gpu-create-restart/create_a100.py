#!/usr/bin/python
# This is a simple example of how to request an instance with a GPU using the notebook API. May contain bugs, for reference purposes only.

from google.cloud import notebooks_v1
from google.api_core import exceptions as core_exceptions
import datetime

def create_notebook_instance(request):
    try: 
        print(datetime.datetime.now())
        operation = client.create_instance(request=request)
        print("Waiting for operation to complete...")
        response = operation.result()
        return response
    except core_exceptions.ServiceUnavailable as e:
        print(e)
        print("Unavailable, trying again...")
        return None

if __name__ == '__main__':

    # Ref: https://cloud.google.com/python/docs/reference/notebooks/latest/google.cloud.notebooks_v1.services.notebook_service.NotebookServiceClient
    client = notebooks_v1.NotebookServiceClient()

    # Ref:. https://cloud.google.com/python/docs/reference/notebooks/latest/google.cloud.notebooks_v1.types.CreateInstanceRequest
    request = {
        'parent': 'projects/YOU_PROJECT_ID/locations/us-central1-a',
        'instance_id': 'pytorch2-a100',
        'instance': { # ref.: https://cloud.google.com/python/docs/reference/notebooks/latest/google.cloud.notebooks_v1.types.Instance
            'install_gpu_driver': True,
            'service_account': "000000000000-compute@developer.gserviceaccount.com",
            'tags': ['allow-ssh'],
            'network': 'projects/YOU_PROJECT_ID/global/networks/default', #vpc name: 'default'
            'subnet': 'projects/YOU_PROJECT_ID/regions/us-central1/subnetworks/default', #subnetwork name 'default'
            'machine_type': 'a2-highgpu-1g',
            'boot_disk_size_gb': 256,
            'boot_disk_type': notebooks_v1.Instance.DiskType.PD_SSD,
            'data_disk_size_gb': 512,
            'data_disk_type': notebooks_v1.Instance.DiskType.PD_SSD,
            'vm_image': { #Ref. https://cloud.google.com/deep-learning-vm/docs/images#listing-versions 
                'image_name': "pytorch-2-2-cu121-notebooks-v20240319-debian-11-py310",
                'project': "deeplearning-platform-release"
            }
        }
    }

    # Loop
    status = None
    while(status == None):
        status = create_notebook_instance(request)
        print(status)

