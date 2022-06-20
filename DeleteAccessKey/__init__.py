import logging
import os
import azure.functions as func
import boto3
from botocore.exceptions import ClientError


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    accesskeyid = req.params.get('accesskeyid')
    username = req.params.get('username')
    if accesskeyid and username:
        logging.getLogger().setLevel(logging.INFO)
        logging.info('Starting program')
        try:
            # Create IAM client
            iam = boto3.client('iam',
                               aws_access_key_id=os.environ["AWS_AccessKeyId"],
                               aws_secret_access_key=os.environ["AWS_SecretAccessKey"])
            try:
                # Delete access key
                iam.delete_access_key(AccessKeyId=accesskeyid, UserName=username)
            except iam.exceptions.LimitExceededException or iam.exceptions.NoSuchEntityException as err:
                return func.HttpResponse(str(err), status_code=400)
            except iam.exceptions.ServiceFailureException as err:
                return func.HttpResponse(str(err), status_code=500)
            return func.HttpResponse("Successfully deleted.", status_code=200)
        except ClientError as err:
            return func.HttpResponse(str(err), status_code=400)
    else:
        return func.HttpResponse("Please pass an accesskeyid and a username on the query string", status_code=400)
