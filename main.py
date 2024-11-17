import pandas as pd

# Specify the path to your CSV file
csv_file_path = 'files/Filtered_mega_investor_data.csv'

# Specify the desired path for the output Excel file
xlsx_file_path = 'files/output_single_row.xlsx'

# Read only the first row of the CSV file
data = pd.read_csv(csv_file_path, nrows=1)

# Write the single row to an Excel file
data.to_excel(xlsx_file_path, index=False)

print(f"First row has been successfully converted to Excel and saved at: {xlsx_file_path}")
