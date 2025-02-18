import os
import boto3
from dotenv import load_dotenv
from client_reddit import ClientReddit

load_dotenv()

# Inicializa o cliente do Reddit
reddit = ClientReddit(
    client_id=os.environ.get("REDDIT_CLIENT_KEY"),
    client_secret=os.environ.get("REDDIT_SECRET_KEY"),
    username=os.environ.get("REDDIT_USERNAME"),
    password=os.environ.get("REDDIT_PASSWORD"),
    user_agent=os.environ.get("REDDIT_USER_AGENT"),
)

df_posts = reddit.get_hot_posts(
    os.environ.get("REDDIT_SUBREDDIT"),
    limit=10,
)
CSV_PATH = f"{os.environ.get("REDDIT_SUBREDDIT")}.csv"
df_posts.to_csv(CSV_PATH, index=False)


# Escrevendo no S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)
bucket_name = os.environ.get("AWS_S3_BUCKET")
s3.upload_file(CSV_PATH, bucket_name, f"subreddits_raw/{CSV_PATH}")