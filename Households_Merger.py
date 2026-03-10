import pandas as pd
import glob
import os

folder_path = './inputs' 
output_filename = './outputs/Merge_Households.csv'
all_files = glob.glob(os.path.join(folder_path, "*.xls"))

if not all_files:
    print("No .xls files found.")
else:
    all_dataframes = []

    for file in all_files:
        print(f"Processing: {file}")
        try:
            # Attempt 1: Standard Excel reading
            df = pd.read_excel(file)
        except ValueError:
            try:
                # Attempt 2: If it's actually an HTML table disguised as .xls
                print(f"  --> Format tricky, trying HTML engine...")
                df_list = pd.read_html(file)
                df = df_list[0] # Take the first table found
            except Exception as e:
                print(f"  [!] Failed to read {file}: {e}")
                continue
        
        df['source_file'] = os.path.basename(file)
        all_dataframes.append(df)

    if all_dataframes:
        merged_df = pd.concat(all_dataframes, ignore_index=True)
        merged_df.to_csv(output_filename, index=False)
        print(f"\nSuccess! Merged into {output_filename}")
    else:
        print("No data was successfully recovered.")
        