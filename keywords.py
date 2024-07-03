from openai import OpenAI
import json
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import requests
import os

dotenvpath = find_dotenv()
load_dotenv(dotenvpath)

OPENAI_API_KEY = os.getenv('OpenAI_KEY')
client = OpenAI(api_key = OPENAI_API_KEY)

df = pd.read_csv("outlet_products.csv")

new_df = pd.DataFrame(columns=['SKU', 'ProductDescription', 'ProductMetaTitle', 'ProductMetaDescription', 'SEOKeywords'])
print(type(new_df))

# For each row in our CSV file, we'll find relevant SEO keywords and optimise our meta data and product description.
for index, row in df.iterrows():
    description = row["ProductDescription"]
    mTitle = row["ProductMetaTitle"]
    mDescription = row["ProductMetaDescription"]
    sku = row["ProductNumber"]

    # Extract initial set of keywords from the product title and description
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract SEO keywords from the provided product title and description. These keywords should be ones that people might search online to find this product. Provide the keywords separated by comma but no space after comma"
            },
            {
                "role": "user",
                "content": f"Product Title: {mTitle}\nProduct description: {mDescription}"
            }
        ]
    )
    keywords = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "From the provided keywords, remove all the keywords that mention happy socks or any other brand name."
            },
            {
                "role": "user",
                "content": f"Keywords: {completion.choices[0].message.content}"
            }
        ]
    )
    print("Extracted keywrods from the product title and description")

    # Get SEO keywrods from the API
    try:
        response = requests.get(f"http://127.0.0.1:5000/keyword-ideas?keyword={keywords}")
    except:
        print("Error in getting SEO keywords from the API")
    
    print("Got SEO keywords from the API")
    output = json.loads(response.text)
    seoKeywords = ', '.join(output)

    new_row = {'SKU': sku, 'ProductDescription': description, 'ProductMetaTitle': mTitle, 'ProductMetaDescription': mDescription, 'SEOKeywords': seoKeywords }
    new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)

    
# Save the keyword and product date to new csv file
new_df.to_csv("product_keywords.csv", index=False)
print("Saved the product data to product_keywords.csv file")