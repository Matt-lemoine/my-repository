# This code is to help analyze the csv that is output from the main_TDA.py code

""""
created: Matthew Lemoine
date: 6-1-2025

This code takes in the CSV that is output from the main_TDA.py code and tells you an outline of the way that the clusters are joining up.

Input:
- The CSV from the main_TDA.py that has the 0-dim'l components and the clusters in those components.

Output:
- A CSV file that tells you the following:
    - Clusters that are significant (i.e. persist for a while, or eat all ther other clusters)
    - The basic stats in each of the clusters as they get bigger
    - If there are fingers.
"""

import pandas as pd
import numpy as np
import ast
import csv

# This string is for de-bugging only.
gh = 'The code got here'

input_csv = input('What is the name of the CSV from main_TDA.py that has only the 0-diml information? ')
length_of_dataset = input('What is the length of the original dataset? ')

# Step 1: Load the CSV and make sure that it can read what is written.

data = pd.read_csv(input_csv)
def load_and_validate_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        if not np.issubdtype(df.to_numpy().dtype, np.number):
            raise ValueError("The CSV file contains non-numerical values.")
        data_array = df.to_numpy()
        if data_array.size == 0:
            raise ValueError("The CSV file is empty.")
        return data_array
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        raise
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        raise
    except ValueError as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__": #if __name__ == "__main__": checks if the script is being run directly. If true, the code block following it will execute.
    filepath=input_csv
    try:
        data_array = load_and_validate_csv(filepath)
        print("CSV loaded successfully.")
        # Call other scripts or functions here
    except Exception as e:
        print(f"Failed to load and validate data: {e}")

# Step 2: We need to now look at the clusters. The data will already be organized in increasing length of bar from the barcode.

# The first thing that we want to do is find the biggest clusters and analyze those first.

column = 4

# Convert the string in {} to a Python set using ast.literal_eval
input_csv[column] = input_csv[column].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else set())

# Add a column for the size of the sets
input_csv["list_size"] = input_csv[column].apply(len)

# Sort by size
input_csv = input_csv.sort_values(by="list_size", ascending=False)

# Filter rows with list size >= threshold
threshold = 0.25*length_of_dataset
input_csv = input_csv[input_csv["list_size"] >= threshold]

# Drop the helper column if desired
input_csv = input_csv.drop(columns=["list_size"])

# Parse sets
input_csv[column] = input_csv[column].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else set())
input_csv["list_size"] = input_csv[column].apply(len)

# Sort by size (largest first to preserve bigger sets)
df = input_csv.sort_values(by="list_size", ascending=False).reset_index(drop=True)

# Mark rows to keep
keep_indices = set(df.index)

# Compare all pairs
for i in df.index:
    if i not in keep_indices:
        continue
    set_i = df.at[i, column]
    for j in range(i + 1, len(df)):
        if j not in keep_indices:
            continue
        set_j = df.at[j, column]

        # Compare overlap
        intersection = set_i & set_j
        if len(intersection) > 0.5 * len(set_j):  # compare to smaller set
            keep_indices.discard(j)  # drop the smaller one (later in sort)

# Keep only the selected rows
df = df.loc[sorted(keep_indices)].reset_index(drop=True)
df = df.drop(columns=["list_size"])

# Save result
df.to_csv("deduplicated.csv", index=False)