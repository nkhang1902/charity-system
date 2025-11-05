import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    def __init__(self):
        self.AWSRegion = os.getenv("AWS_REGION", "ap-southeast-2")

        self.S3BucketName = os.getenv("S3_BUCKET_NAME")

        self.MySQLHost = os.getenv("MYSQL_HOST")
        self.MySQLPort = int(os.getenv("MYSQL_PORT", 3306))
        self.MySQLUser = os.getenv("MYSQL_USER", "root")
        self.MySQLPassword = os.getenv("MYSQL_PASSWORD", "")
        self.MySQLDatabase = os.getenv("MYSQL_DATABASE", "db")

        self.JWTSecret = os.getenv("JWT_SECRET_KEY", "open-api-secret")
        self.JWTExpiredHours = int(os.getenv("JWT_EXPIRED_IN_HOURS", 1))

settings = Settings()