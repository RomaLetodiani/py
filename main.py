import pandas as pd
import os

# Specify the path to your JSON file
file_path = 'files/investor_110k_data.json'
output_file_path = 'files/investor_110k_data_p.json'

# Check if the file is not empty
if os.path.getsize(file_path) > 0:
    # Read the JSON file
    data = pd.read_json(file_path)
else:
    raise ValueError("The JSON file is empty")

def analyze_data():
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


def check_duplicates():
    # Check for duplicates in the 'id' column
    duplicates = data[data.duplicated('id')]

    if not duplicates.empty:
        print("Duplicates found in the 'id' column:")
        print(len(duplicates))
    else:
        print("No duplicates found in the 'id' column")