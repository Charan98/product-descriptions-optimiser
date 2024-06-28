# Keyword Research and Content Generation Workflow

Using Open AI and Google Keyword Planner, generating SEO optimised content for ecommerce. 

## Workflow
1. Export products in a csv file that has the followng fields - ProductTitle, SKU, ProductDescription, ProductMetaTitle, ProductMetaDescription
2. Run the keywords.py. This will find SEO keywrods for all your products in the CSV and store it in a new file product_keywrods.csv
3. Verify the keywords returned by the API and remove the ones that are not relevant or needed.
4. Run descriptions.py. This will rewrite your content using the SEO keywords and save them to optimised_products.csv
