#%%
import pandas as pd

# Read the edge table from a CSV file
edges_df = pd.read_csv('/Users/Arundhati/Downloads/US All Genre Collaborations.csv')
#%%
# Sum the values in the 'weight' column based on unique combinations of 'Source' and 'Target'
edges_df['Weight'] = edges_df.groupby(['source', 'target'])['weight'].transform('sum')

# Remove duplicates based on 'Source' and 'Target' columns
edges_df = edges_df.drop_duplicates(subset=['source', 'target'])

# Save the updated edge DataFrame to a different directory
edges_df.to_csv(r'/Users/Arundhati/Downloads/US_Genre_edges_with_summed_weights.csv', index=False, header=True)
print('done')

# Print the updated edge DataFrame
print("Edge DataFrame with Summed Weight Column:")
print(edges_df)

# %%
