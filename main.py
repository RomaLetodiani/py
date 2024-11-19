import pandas as pd
import os

# Specify the path to your JSON file
file_path = 'files/investor_110k_data.json'
output_file_path = 'files/investor_110k_data_p.json'

# Check if the file is not empty
if os.path.getsize(output_file_path) > 0:
    # Read the JSON file
    data = pd.read_json(output_file_path)
else:
    raise ValueError("The JSON file is empty")

def processes_data():
    """
    Processes a DataFrame of investor data to remove duplicates and update certain fields.
    This function performs the following steps:
    1. Iterates over the rows of the DataFrame to identify and remove duplicate investors based on their 'id'.
    2. Extracts and processes various fields from each investor record, including emails, LinkedIn, city, country, state, company, past investments, markets, stages, and investor types.
    3. Updates the investor records with new keys indicating the presence of emails and LinkedIn profiles, and replaces nested dictionaries with their 'title' values.
    4. Deletes unnecessary keys ('foundedCompanies' and 'pipelines') from the investor records.
    5. Prints the number of duplicates, unique investors, and the number of investors before and after removing duplicates.
    6. Converts the processed list of investor records back to a DataFrame and saves it to a JSON file.
    Note:
        - The input DataFrame `data` and the output file path `output_file_path` are assumed to be defined outside this function.
    """
    new_data = []

    set_ids = set()
    duplicated_ids = set()

    # Iterate over the rows of the DataFrame
    for _, investor in data.iterrows():
        investor_id = investor.get('id', None)
        if investor_id in set_ids:
            duplicated_ids.add(investor_id)
            continue
        else:
            set_ids.add(investor_id)

        emails = investor.get('emails', [])
        linkedin = investor.get('linkedin', None)
        city = investor.get('city', {})
        city_title = city.get('title', '')
        country = investor.get('country', {})
        country_title = country.get('title', '')
        state = investor.get('state', {})
        state_title = state.get('title', '')
        company = investor.get('company', {})
        company_title = company.get('title', '')

        pastInvestments_raw = investor.get('pastInvestments', [])
        pastInvestments = []

        for investment in pastInvestments_raw:
            investment_title = investment.get('title', '')
            pastInvestments.append(investment_title)

        markets_raw = investor.get('markets', [])
        markets = []

        for market in markets_raw:  
            market_title = market.get('title', '')
            markets.append(market_title)

        stages_raw = investor.get('stages', [])
        stages = []

        for stage in stages_raw:
            stage_title = stage.get('title', '')
            stages.append(stage_title)

        investorTypes_raw = investor.get('investorTypes', [])
        investorTypes = []

        for investorType in investorTypes_raw:
            investorType_title = investorType.get('title', '')
            investorTypes.append(investorType_title)

        # Add new keys to a copy of the investor record
        updated_investor = investor.to_dict()
        updated_investor['hasEmail'] = len(emails) > 0
        updated_investor['hasLinkedin'] = linkedin is not None
        updated_investor['city'] = city_title
        updated_investor['country'] = country_title
        updated_investor['state'] = state_title
        updated_investor['company'] = company_title
        updated_investor['pastInvestments'] = pastInvestments
        updated_investor['markets'] = markets
        updated_investor['stages'] = stages
        updated_investor['investorTypes'] = investorTypes

        # Delete the unnecessary keys
        del updated_investor['foundedCompanies']
        del updated_investor['pipelines']

        new_data.append(updated_investor)

    print(f"Number of duplicates: {len(duplicated_ids)}")

    print(f"Number of unique investors: {len(set_ids)}")

    print(f"Number of investors after removing duplicates: {len(new_data)}")

    print(f"Number of investors before removing duplicates: {len(data)}")
    # Convert the list of dictionaries back to a DataFrame
    new_data_df = pd.DataFrame(new_data)

    # Save the new DataFrame to a JSON file
    new_data_df.to_json(output_file_path, orient='records', indent=4)

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

def check_duplicates():
    # Check for duplicates in the 'id' column
    duplicates = data[data.duplicated('id')]

    if not duplicates.empty:
        print("Duplicates found in the 'id' column:")
        print(len(duplicates))
    else:
        print("No duplicates found in the 'id' column")