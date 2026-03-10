import pandas as pd

# 1. Load the individuals data
# Using sep=None to handle potential tab/comma inconsistencies
df = pd.read_csv('./inputs/Individuals.csv', sep=None, engine='python')

# 2. Clean up column names and data to avoid matching errors
df.columns = df.columns.str.strip()
df['Family Code'] = df['Family Code'].astype(str).str.strip()
df['Relationship to Household Head'] = df['Relationship to Household Head'].astype(str).str.strip()

# 3. Define what we are looking for
# We group by 'Family Code' and check if 'Head' exists in the 'Relationship' column
family_heads = df.groupby('Family Code')['Relationship to Household Head'].apply(lambda x: (x == 'Head').any())

# 4. Identify families missing a head
missing_head_codes = family_heads[family_heads == False].index.tolist()

if not missing_head_codes:
    print("✅ Success: Every family has a designated 'Head'.")
else:
    print(f"⚠️ Found {len(missing_head_codes)} families missing a 'Head'.")
    
    # 5. Create a report of the problematic records
    missing_df = df[df['Family Code'].isin(missing_head_codes)]
    
    # Sort by Family Code so you can see the groups clearly
    missing_df = missing_df.sort_values(by='Family Code')
    
    # Save the problematic records to a CSV for manual fixing
    output_file = './outputs/Families_Missing_Heads.csv'
    missing_df.to_csv(output_file, index=False)
    
    print(f"Details of these families have been saved to: {output_file}")
    
    # Show the first few problematic codes
    print("\nFirst few Family Codes missing a Head:")
    for code in missing_head_codes[:10]:
        print(f" - {code}")