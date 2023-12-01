import kfp
from kfp.dsl import component
from kfp import dsl
from kfp.dsl import (Dataset, Input, Metrics, Model, Output)

@component(base_image="python:3.10", packages_to_install=["google-cloud-dataform"])
def dataform_op(repository:str, compilation_results_id: str, op_timeout:int=300) -> str:

    from google.cloud import dataform_v1beta1
    import time
    
    client = dataform_v1beta1.DataformClient()
    
    # Run workflow
    request = dataform_v1beta1.CreateWorkflowInvocationRequest(
    parent=repository,
    workflow_invocation=dataform_v1beta1.types.WorkflowInvocation(
        compilation_result=compilation_results_id)
    )
    response = client.create_workflow_invocation(request=request)

    # wait to finish
    timeout_start = time.time()
    while time.time() < timeout_start + op_timeout:
        response = client.get_workflow_invocation(
            request=dataform_v1beta1.GetWorkflowInvocationRequest(name=response.name)
        )
        
        if(response.state != dataform_v1beta1.types.WorkflowInvocation.State.RUNNING): break

    return str(response)


@dsl.pipeline(
  name='dataform-op-pipeline',
  description='Test pipeline for triggering dataform')
def pipeline(repository:str, compilation_results_id: str, op_timeout:int):
    
    op1 = dataform_op(repository=repository, compilation_results_id=compilation_results_id, op_timeout=op_timeout)
    op1.set_display_name("Dataform workflow id:"+str(compilation_results_id))
    

kfp.compiler.Compiler().compile(pipeline, package_path='pipeline.yaml')

import google.cloud.aiplatform as aip
import logging

logging.getLogger().setLevel(logging.DEBUG)

aip.init(project="XXXXXXXXX", staging_bucket="gs://XXXXXXXXXXXXXXXXXXXX")

job = aip.PipelineJob(
    display_name="dataform-pipeline",
    template_path="pipeline.yaml",
    pipeline_root="gs://XXXXXXXXXXXXXXXXXXXX/pipeline-root/dataform-pipeline",
    enable_caching=True,
    failure_policy = 'fast',
     parameter_values={
         "repository": "projects/XXXXXXXXXX/locations/us-east1/repositories/dataform-test-1", 
         "compilation_results_id": "projects/XXXXXXXXXX/locations/us-east1/repositories/dataform-test-1/compilationResults/6f4fb988-66cb-45f2-9149-XXXXXXXXXXXX",
         "op_timeout": 600
    }
)

job.run()

