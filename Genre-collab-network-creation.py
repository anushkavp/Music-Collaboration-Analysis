#%%

import pandas as pd

# Load artist collaboration network data
artist_collaboration_df = pd.read_csv('/Users/anushkavuppala/Documents/Anushka/GWU/Fall 2023/Capstone/Music dataset/Artist Collaboration Network/global/global-artist_network-2019.csv',sep="\t")

# Load artist data
artist_data_df = pd.read_csv('/Users/anushkavuppala/Documents/Anushka/GWU/Fall 2023/Capstone/Music dataset/Artists/spotify_artists_info_complete.csv',on_bad_lines='skip', sep="\t")

print(artist_collaboration_df.head())
print(artist_data_df.head())
#%%
# Merge the datasets based on Artist IDs
merged_df = pd.merge(artist_collaboration_df, artist_data_df, left_on='artist_1', right_on='name')
merged_df = pd.merge(merged_df, artist_data_df, left_on='artist_2', right_on='name', suffixes=('_Artist1', '_Artist2'))

# Select relevant columns for the genre collaboration network
genre_collaboration_df = merged_df#[['Name_Artist1', 'Genres_Artist1', 'Name_Artist2', 'Genres_Artist2', 'Count of songs', 'Song ID']]

print(genre_collaboration_df)
# Save the genre collaboration network to a CSV file
#genre_collaboration_df.to_csv('genre_collaboration_network_2019.csv', index=False)

# %%
import ast 
def extract_first_genre(genre_list):
    genres = ast.literal_eval(genre_list)
    if isinstance(genres, list) and genres:
        return genres[0]
    else:
        return None

merged_df['genre_Artist1'] = merged_df['genres_Artist1'].apply(extract_first_genre)
merged_df['genre_Artist2'] = merged_df['genres_Artist2'].apply(extract_first_genre)

print("=======")
# Select relevant columns for the genre collaboration network
genre_collaboration_df = merged_df[['name_Artist1', 'genre_Artist1', 'name_Artist2', 'genre_Artist2']]
print(genre_collaboration_df.head())

#%%
# Save the genre collaboration network to a CSV file
genre_collaboration_df.to_csv('genre_collaboration_network_2019.csv', index=False)
# %%
