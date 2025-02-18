import os
import json
import boto3
import pandas as pd
from openai import OpenAI

# Instantiate the OpenAI client.
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


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

def lambda_handler(message, context):   
    message["sentiment"] = classificar_sentimento(message["title"] + message["text"])
    return message
