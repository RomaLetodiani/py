import pandas as pd

# Specify the path to your CSV file
csv_file_path = 'files/corrected_investors_data.csv'

file_path = 'files/output_single_row'

# Read only the first row of the CSV file
data = pd.read_csv(csv_file_path, nrows=1)

def convert_to_json():
    data.to_json(f'{file_path}.json', orient='records', lines=True)
    print(f"Successfully converted to Excel and saved at: {file_path}.json")

def convert_to_excel():
    data.to_excel(f'{file_path}.xlsx', index=False)
    print(f"Successfully converted to Excel and saved at: {file_path}.xlsx")