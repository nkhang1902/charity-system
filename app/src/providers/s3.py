import boto3
from app.src.core.config import settings

class S3:
    def __init__(self):
        try:
            self.s3Client = boto3.client('s3', region_name=settings.AWSRegion)
            self.bucketName = settings.S3BucketName
        except Exception as e:
            print(f"Unexpected error during S3 initialization: {str(e)}")

    def getFile(self, filePath: str):
        try:
            response = self.s3Client.get_object(Bucket=self.bucketName, Key=filePath)
            return response["Body"].read()
        except Exception as e:
            print(f"Error fetching file {filePath} from {self.bucketName}: {e}")
            return None

    def checkFileExists(self, filePath: str):
        try:
            if self.s3Client.head_object(Bucket=self.bucketName, Key=filePath):
                return True
            else:
                return False
        except Exception as e:
            print(f"Error fetching file {filePath} from {self.bucketName}: {e}")
            return False
