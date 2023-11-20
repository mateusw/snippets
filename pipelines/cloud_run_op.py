@component(base_image="python:3.10", packages_to_install=["google-cloud-iam", "urllib3", "requests"])
def cloud_run_op(endpoint_url:str, target_audience:str) -> str:

    import time
    import urllib
    import google.auth.transport.requests
    from google.cloud import iam_credentials_v1
    import base64
    import time
    import json
    import logging
    import ssl

    # activate debugging mode
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.DEBUG)
    urllib.request.HTTPHandler(debuglevel=1)

    # Get service account address
    metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email"
    req = urllib.request.Request(metadata_url)
    req.add_header("Metadata-Flavor", "Google")
    sa = urllib.request.urlopen(req).read().decode("utf-8") 

    # Get ID Token
    iam_client = iam_credentials_v1.IAMCredentialsClient()
    name = "projects/-/serviceAccounts/{}".format(sa)
    id_token = iam_client.generate_id_token(request={"name":name, "audience" :target_audience}).token

    # Request
    ctx = ssl.create_default_context()
    ctx.set_ciphers('DEFAULT')
    req = urllib.request.Request(endpoint_url)
    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)
    return str(response.read())

