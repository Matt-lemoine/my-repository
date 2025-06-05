import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

# Load data from CSV file
df = pd.read_csv("MORT_The Midwest_(no dates (use)).csv")

# Optional: If your CSV has a column with labels (like names), extract and drop it
# labels = df["label_column_name"]
# df = df.drop("label_column_name", axis=1)

df = df.to_numpy() 

def z_score_normalize(data): #the function to normalize the data
    mean_val = np.mean(data, axis=0)
    std_val = np.std(data, axis=0)
    normalized_data = (data - mean_val) / std_val
    return normalized_data

df = z_score_normalize(df)

# Compute linkage matrix
Z = linkage(df, method='single')

# Plot dendrogram
plt.figure(figsize=(10, 5))
dendrogram(Z)  # You can add labels=labels if you extracted them
plt.title("Dendrogram from CSV Data")
plt.xlabel("Sample Index")
plt.ylabel("Distance")
plt.tight_layout()
plt.show()
