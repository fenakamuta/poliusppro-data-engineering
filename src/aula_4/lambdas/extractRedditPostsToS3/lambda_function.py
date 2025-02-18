import os
import csv
import boto3
import pandas as pd
from datetime import datetime
from reddit_extractor import search_posts_by_text


def lambda_handler(event, context):
    aws_s3_bucket = event.get("aws_s3_bucket")
    topic = event.get("topic")
    n_posts = int(event.get("n_posts", 10))
    csv_path = f"/tmp/{topic}.csv"
    object_path = f"topics_raw/{topic}/{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.csv"

    posts = search_posts_by_text(
        search_text=topic,
        n_posts=n_posts,
        sort="new"
    )

    df_posts = pd.DataFrame(posts)
    df_posts["topic"] = topic
    df_posts.to_csv(
        csv_path,
        index=False,
        quoting=csv.QUOTE_ALL,
        escapechar="\\",
        quotechar='"'
    )

    s3 = boto3.client("s3")
    bucket_name = aws_s3_bucket
    s3.upload_file(csv_path, bucket_name, object_path)

    return {
        "statusCode": 200,
        "topic": topic,
        "bucket": aws_s3_bucket,
        "object_path": object_path,
        "body": str(df_posts.shape),
        "s3_path": f"s3://{aws_s3_bucket}/{object_path}",
    }