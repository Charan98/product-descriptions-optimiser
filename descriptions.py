from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import os

dotenvpath = find_dotenv()
load_dotenv(dotenvpath)

OPENAI_API_KEY = os.getenv('OpenAI_KEY')

client = OpenAI(api_key = OPENAI_API_KEY)

df = pd.read_csv("product_keywords.csv")

new_df = pd.DataFrame(columns=['SKU', 'ProductDescription', 'ProductMetaTitle', 'ProductMetaDescription', 'SEOKeywords', 'OptimisedMetaTitle', 'OptimisedMetaDescription', 'OptimisedDescription'])
print(type(new_df))

# For each row in our CSV file, we'll find relevant SEO keywords and optimise our meta data and product description.
for index, row in df.iterrows():
    description = row["ProductDescription"]
    mTitle = row["ProductMetaTitle"]
    mDescription = row["ProductMetaDescription"]
    sku = row["SKU"]
    seoKeywords = row["SEOKeywords"]

    # Optimise content using the SEO keywords
    print("Starting optimisation of meta title, meta description and product description")
    generateMTitle = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Generate a new meta title based on the provided product title and SEO keywords. The meta title should be strictly less than 60 characters long."
            },
            {
                "role": "user",
                "content": f"Product Title: {mTitle}\nSEO Keywords: {seoKeywords}"
            }
        ]
    )
    optimisedMetaTitle = generateMTitle.choices[0].message.content

    generateMDescription = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Generate a new meta description based on the provided product title and SEO keywords. The description should be strictly less than 155 characters long."
            },
            {
                "role": "user",
                "content": f"Product Title: {mDescription}\nSEO Keywords: {seoKeywords}"
            }
        ]
    )
    optimisedMetaDescription = generateMDescription.choices[0].message.content

    generateDescription = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Generate a new product description based on the provided product title and SEO keywords. Keep the description to 300 characters long. Avoid mentioning any other brands except for happysocks"
            },
            {
                "role": "user",
                "content": f"Product Title: {mDescription}\nSEO Keywords: {seoKeywords}"
            }
        ]
    )
    optimisedDescription = generateDescription.choices[0].message.content

    # Store the information in the new data frame
    new_row = {'SKU': sku, 'ProductDescription': description, 'ProductMetaTitle': mTitle, 'ProductMetaDescription': mDescription, 'SEOKeywords': seoKeywords, 'OptimisedMetaTitle': optimisedMetaTitle, 'OptimisedMetaDescription': optimisedMetaDescription, 'OptimisedDescription': optimisedDescription}
    new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)
    

print("Optimisation complete! File saved as optimised_products.csv")
new_df.to_csv("optimised_products.csv", index=False)

