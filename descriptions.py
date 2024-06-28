from openai import OpenAI
import pandas as pd
import numpy as np
import requests
import os

dotenvpath = find_dotenv()
load_dotenv(dotenvpath)

OPENAI_API_KEY = os.getenv('OpenAI_KEY')

response = requests.get("http://127.0.0.1:5000/keyword-ideas?keyword=mens socks")
print(response.text)

client = OpenAI(api_key = OPENAI_API_KEY)

mTitle = "Mens Socks"
mDescription = "Men"

completion = client.chat.completions.create(
    model="gtp-40",
    messages=[
        {
            "role": "system",
            "content": "Extract SEO keywords from the provided product title and description. These keywords should be ones that people might search online to find this product. Provide the keywords separated by comma but no space after comma"
        },
        {
            "role": "user"
            "content": "Product Title:" "Product description:" 
        }
    ]
)
print(completion.choices[0].message)


