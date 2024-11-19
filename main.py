import pandas as pd
import os

# Specify the path to your JSON file
file_path = 'files/investor_110k_data.json'

output_file_path = 'files/investor_110k_data'

# Check if the file is not empty
if os.path.getsize(file_path) > 0:
    # Read the JSON file
    data = pd.read_json(file_path)
else:
    raise ValueError("The JSON file is empty")

def analyze_data():
    no_email_count = 0
    yes_email_count = 0
    no_linkedin_count = 0
    yes_linkedin_count = 0

    yes_email_no_linkedin = 0
    no_email_yes_linkedin = 0

    yes_email_yes_linkedin = 0
    no_email_no_linkedin = 0

    # Iterate over the rows of the DataFrame
    for _, investor in data.iterrows():
        emails = investor['emails']
        has_email = len(emails) > 0
        has_linkedin = investor['linkedin'] is not None

        if has_email:
            yes_email_count += 1
            if has_linkedin:
                yes_email_yes_linkedin += 1
            else:
                yes_email_no_linkedin += 1
        else:
            no_email_count += 1
            if has_linkedin:
                no_email_yes_linkedin += 1
            else:
                no_email_no_linkedin += 1

        if has_linkedin:
            yes_linkedin_count += 1
        else:
            no_linkedin_count += 1

    print(f"Total number of investors: {len(data)}")

    print(f"Number of investors without email: {no_email_count}")
    print(f"Number of investors without LinkedIn: {no_linkedin_count}")
    print(f"Number of investors with email: {yes_email_count}")
    print(f"Number of investors with LinkedIn: {yes_linkedin_count}")

    print(f"Number of investors with email but no LinkedIn: {yes_email_no_linkedin}")
    print(f"Number of investors with no email but with LinkedIn: {no_email_yes_linkedin}")
    print(f"Number of investors with email and LinkedIn: {yes_email_yes_linkedin}")
    print(f"Number of investors with no email and no LinkedIn: {no_email_no_linkedin}")

# Run the analysis
analyze_data()
