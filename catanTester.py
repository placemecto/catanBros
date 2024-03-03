import pandas as pd
import numpy as np

# Step 1: Read the CSV file
df = pd.read_csv('catanReport_Cleaned.csv')

# Step 2: Add a new column with empty values
df['H'] = np.nan

# Step 3: Save the DataFrame back to a CSV file
df.to_csv('CatanReport_Cleaned.csv', index=False)
