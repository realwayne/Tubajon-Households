import pandas as pd

# 1. Load the files
# Note: Using sep=None allows pandas to guess if it's Tabs or Commas automatically
households = pd.read_csv('./outputs/Merge_Households.csv', sep=None, engine='python')
individuals = pd.read_csv('./inputs/Individuals.csv', sep=None, engine='python')

# 2. Clean up the BuildingCode column 
# (Ensures both are treated as strings to avoid matching errors)
households['Unique Code'] = households['Unique Code'].astype(str).str.strip()
individuals['Building Code'] = individuals['Building Code'].astype(str).str.strip()

# 3. Identify missing households
# We look for BuildingCodes in households that are NOT in the individuals list
missing_households = households[~households['Unique Code'].isin(individuals['Building Code'])]

# 4. Save the result
output_file = './outputs/Households_With_No_Individuals.csv'
missing_households.to_csv(output_file, index=False)

# 5. Summary Report
print(f"Total Households scanned: {len(households)}")
print(f"Households with matching individuals: {len(households) - len(missing_households)}")
print(f"---")
print(f"Found {len(missing_households)} households with NO individual records.")
print(f"Results saved to: {output_file}")

# Optional: Print the first few missing codes to the console
if len(missing_households) > 0:
    print("\nFirst few missing BuildingCodes:")
    print(missing_households['Unique Code'].head().to_string(index=False))