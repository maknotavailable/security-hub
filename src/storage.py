import boto3 as b3
import os
import json
import logging
# from azure.storage.blob import BlockBlobService

import utils

# Format logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s')


class Cloud():
    def __init__(self, destination: str = "s3"):
        """

        Possible destinations:
        - s3 (AWS)
        - blob (Azure)

        """

        self.destination = destination

        if destination == "blob":
            # Run Azure blob storage upload
            # self.block_blob_service = BlockBlobService(
            # account_name=config['blob']['account'], account_key=config['blob']['key'])
            pass
        elif destination == "s3":

            # AWS access
            ACCESS_KEY = utils.get_secret("ACCESS_KEY_ID", "aws")
            SECRET_KEY = utils.get_secret("SECRET_ACCESS_KEY", "aws")
            AWS_REGION = utils.get_secret("REGION", "aws")
            self.S3_BUCKET = utils.get_secret("S3_BUCKET", "aws")

            # Run AWS S3 upload
            self.client = b3.client('s3',
                                    aws_access_key_id=ACCESS_KEY,
                                    aws_secret_access_key=SECRET_KEY,
                                    region_name=AWS_REGION)

        else:
            log.error(
                "Cloud storage provider %s is not supported. Use 's3' or 'blob' instead." % destination)

    def _upload_blob(self, fp, fn, foldername):
        pass
        # try:
        #     self.block_blob_service.create_blob_from_path(
        #         config['blob'][container_name], fn, fp)
        # except Exception as e:
        #     log.error(' Uploading image failed: %s >> Image stored locally.' % e)
        # else:
        #     log.info('Uploaded image to blob storage: %s' % container_name)

    def _upload_s3(self, fp, fn, foldername):
        filename = foldername + "/" + fn

        # Upload to S3 Bucket on AWS
        try:
            with open(fp, 'rb') as data:
                self.client.upload_fileobj(data, self.S3_BUCKET, filename)
            
            log.info('Uploaded image to: %s' % filename)
            return dict(
                url='https://%s.s3.amazonaws.com/%s' % (self.S3_BUCKET, filename)
            )
        except Exception as e:
            log.error('Uploading image failed: %s >> Image stored locally.' % e)

    def upload(self, filepath: str, foldername: str, remove: bool = True):
        """Orchestrate upload to cloud provider"""

        fn = filepath.split('/')[-1]
        res = dict(
            url = fn
        )

        if self.destination == "blob":
            self._upload_blob(filepath, fn, foldername)

        elif self.destination == "s3":
            res = self._upload_s3(filepath, fn, foldername)
        else:
            raise Exception("Cloud storage provider %s is not supported." % self.destination)

        if remove:
            os.remove(filepath)

        return res