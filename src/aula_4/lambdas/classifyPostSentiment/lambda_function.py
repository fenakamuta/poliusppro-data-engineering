import os
import json
import boto3
import pandas as pd
from openai import OpenAI

# Instantiate the OpenAI client.
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Instantiate the S3 client.
s3_client = boto3.client("s3")

def classificar_sentimento(texto):
    """
    Classify the sentiment of a given text using the OpenAI API.
    Returns one of: "Positivo", "Neutro", or "Negativo".
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Você é uma inteligência artificial especializada em detectar sentimentos de textos.",
            },
            {
                "role": "user",
                "content": f"Classifique o sentimento do seguinte texto em 'Positivo', 'Neutro' ou 'Negativo', retorne apenas uma string: {texto}",
            },
        ],
    )
    # Remove any extraneous whitespace.
    return completion.choices[0].message.content.strip()

def lambda_handler(event, context):
    print(f"Event: {event}")
    if 'Records' not in event:
        return {
            "statusCode": 400,
            "body": "Invalid event format: missing 'Records' key"
        }
    
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    # Download the CSV file from S3 to the /tmp directory.
    input_csv_path = '/tmp/input.csv'
    print(f"Object path: s3://{bucket}/{key}")
    s3_client.download_file(bucket, key, input_csv_path)
    print(f"Downloaded {key} from bucket {bucket}.")

    # Load the CSV into a DataFrame.
    df = pd.read_csv(input_csv_path)
    
    # Enhance the DataFrame: for example, classify sentiment for the "title" column.
    if 'title' in df.columns:
        print("Classifying sentiment for each title...")
        df['sentiment'] = df['title'].astype(str).apply(classificar_sentimento)
    else:
        df['sentiment'] = "N/A"
        print("Column 'title' not found. Marking sentiment as N/A for all rows.")

    # Save the enhanced DataFrame to a new CSV in the /tmp directory.
    enhanced_csv_path = '/tmp/enhanced.csv'
    df.to_csv(enhanced_csv_path, index=False)
    print("Enhanced CSV saved locally.")

    # Determine the new S3 key (for example, changing the folder from raw to enhanced).
    new_key = key.replace("subreddits_raw/", "subreddits_enhanced/")
    
    # Upload the enhanced CSV back to S3.
    s3_client.upload_file(enhanced_csv_path, bucket, new_key)
    print(f"Enhanced CSV uploaded to {bucket}/{new_key}")

    return {
        "statusCode": 200,
        "body": f"Enhanced CSV uploaded to {bucket}/{new_key}"
    }