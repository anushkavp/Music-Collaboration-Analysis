#%% 
import pandas as pd
#%%
# Read the edge table from a CSV file
edges_df = pd.read_csv('/Users/Arundhati/Downloads/All Global Artist Collaborations.csv')
## print(edges_df.head())
#%%
# Count the occurrences of each edge and create a dictionary with edge as key and count as value
edge_counts = edges_df.groupby(['Source', 'Target']).size().reset_index(name='Weight')
edge_counts_dict = {(row['Source'], row['Target']): row['Weight'] for index, row in edge_counts.iterrows()}

# Add the 'Weight' column to the edge DataFrame based on the counts
edges_df['Weight'] = edges_df.apply(lambda row: edge_counts_dict.get((row['Source'], row['Target']), 0), axis=1)

# Remove duplicates based on 'Source' and 'Target' columns
edges_df = edges_df.drop_duplicates(subset=['Source', 'Target'])

# Save the updated edge DataFrame to a different directory
edges_df.to_csv(r'/Users/Arundhati/Downloads/All Global Artists Collab Weights.csv', index = False, header=True)
print('done')


# Print the updated edge DataFrame
print("Edge DataFrame with Count-based Weight Column:")
print(edges_df)

# %%
