import numpy as np
import pandas as pd
import streamlit as st
import base64


def prediction(artist1,artist2,acousticness,danceability,energy,instrumentalness,liveness,loudness,speechiness, valence, tempo):
    import pickle
    import pandas as pd
    track_number=1 # default
    duration_ms = 206557 # mean of train 
    key = 6
    mode = 0
    time_signature = 4 
    acousticness = acousticness
    danceability = danceability
    energy = energy
    instrumentalness = instrumentalness
    liveness = liveness
    loudness = loudness
    speechiness = speechiness
    valence = valence
    tempo = tempo
    artist1 = artist1#"Rea Garvey"
    artist2 = artist2#"Kool Savas"
    release_date_year = 2019
    release_date_month = 11
    release_date_day = 10
    explicit_True = 0
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    X=pd.DataFrame(columns=['track_number', 'duration_ms', 'key', 'mode', 'time_signature',
       'acousticness', 'danceability', 'energy', 'instrumentalness',
       'liveness', 'loudness', 'speechiness', 'valence', 'tempo',
       'followers_artist1', 'popularity_artist1', 'followers_artist2',
       'popularity_artist2', 'artist1_num_available_markets',
       'artist2_num_available_markets', 'release_date_year',
       'release_date_month', 'release_date_day',
       'Weighted_Degree_genre_artist1', 'Degree_genre_artist1',
       'clustering_genre_artist1', 'eigencentrality_genre_artist1',
       'Weighted_Degree_genre_artist2', 'Degree_genre_artist2',
       'clustering_genre_artist2', 'eigencentrality_genre_artist2',
       'clustering_artist1', 'eigencentrality_artist1', 'triangles_artist1',
       'Eccentricity_artist1', 'closnesscentrality_artist1',
       'harmonicclosnesscentrality_artist1', 'betweenesscentrality_artist1',
       'componentnumber_artist1', 'pageranks_artist1', 'Authority_artist1',
       'Hub_artist1', 'clustering_artist2', 'eigencentrality_artist2',
       'triangles_artist2', 'Eccentricity_artist2',
       'closnesscentrality_artist2', 'harmonicclosnesscentrality_artist2',
       'betweenesscentrality_artist2', 'componentnumber_artist2',
       'pageranks_artist2', 'Authority_artist2', 'Hub_artist2',
       'genre_artist1_cluster0', 'genre_artist1_cluster1',
       'genre_artist1_cluster2', 'genre_artist1_cluster3',
       'genre_artist1_cluster4', 'genre_artist1_cluster5',
       'genre_artist1_cluster6', 'genre_artist1_cluster7',
       'genre_artist2_cluster0', 'genre_artist2_cluster1',
       'genre_artist2_cluster2', 'genre_artist2_cluster3',
       'genre_artist2_cluster4', 'genre_artist2_cluster5',
       'genre_artist2_cluster6', 'genre_artist2_cluster7', 'explicit_True'])
    df_artists=pd.read_csv("Music dataset/Artists/spotify_artists_info_complete.csv", sep="\t")
    df_artists.drop("image_url",axis=1,inplace=True)
    df_artists.rename(columns={"name":"artist_name"},inplace=True)
    df_artists.head()
    artist_info = df_artists.loc[df_artists['artist_name'] == artist1]

    genres_artist1="[]"
    followers_artist1=0
    popularity_artist1=0    
    if not artist_info.empty:
        followers_artist1 = artist_info['followers'].values[0]
        popularity_artist1 = artist_info['popularity'].values[0]
        genres_artist1 = artist_info['genres'].values[0]
    else:
        print(f"Artist {artist1} not found in the dataset.")
    
    artist_info = df_artists.loc[df_artists['artist_name'] == artist2]

    genres_artist2="[]"
    followers_artist2=0
    popularity_artist2=0
    if not artist_info.empty:
        followers_artist2 = artist_info['followers'].values[0]
        popularity_artist2 = artist_info['popularity'].values[0]
        genres_artist2 = artist_info['genres'].values[0]
    else:
        print(f"Artist {artist2} not found in the dataset.")
    
    
    preprocessed_table = pd.read_csv("Preprocessed_table-v1.csv")
    filtered_artist = preprocessed_table[preprocessed_table['artist_1'] == artist1]

    # Calculating the average num_available_markets for the given artist_1
    artist1_num_available_markets = filtered_artist['num_available_markets'].mean()

    filtered_artist = preprocessed_table[preprocessed_table['artist_2'] == artist2]

    # Calculating the average num_available_markets for the given artist_2
    artist2_num_available_markets = filtered_artist['num_available_markets'].mean()
    
    import csv

    reader = csv.DictReader(open('Gephi Stats.csv'))
    genre_modularity_mapping={}
    for row in reader:
        genre_modularity_mapping[row['Label']] = int(row['modularity_class'])
    
    genres_artist1 = eval(genres_artist1)
    genres_artist2 = eval(genres_artist2)

    
    from collections import Counter

    def calculate_modularity_class(genre_list):
        modularity_counts = Counter([genre_modularity_mapping.get(genre, 0) for genre in genre_list])

        # Get the modularity class with the maximum count
        max_count = max(modularity_counts.values(), default=0)
        # If there's a tie or no majority, choose the first modularity class
        modularity_class = [mod_class for mod_class, count in modularity_counts.items() if count == max_count]

        # If there's a tie, choose the first modularity class
        if len(modularity_class) > 1:
            return modularity_class[0]
        else:
            # If there's no majority, choose the one that is not 0
            for mod_class in modularity_class:
                if mod_class != 0:
                    return mod_class

            # If all are 0, return 0
            return 0

    modularity_class_artist1 = calculate_modularity_class(genres_artist1)
    modularity_class_artist2 = calculate_modularity_class(genres_artist2)

    def assign_cluster_values(modularity_class, cluster_num):
        if modularity_class == cluster_num:
            return 1
        else:
            return 0

    # Example
    cluster_vars1 = ['genre_artist1_cluster0', 'genre_artist1_cluster1', 'genre_artist1_cluster2',
                    'genre_artist1_cluster3', 'genre_artist1_cluster4', 'genre_artist1_cluster5',
                    'genre_artist1_cluster6', 'genre_artist1_cluster7']
    cluster_vars2 = ['genre_artist2_cluster0', 'genre_artist2_cluster1', 'genre_artist2_cluster2',
                    'genre_artist2_cluster3', 'genre_artist2_cluster4', 'genre_artist2_cluster5',
                    'genre_artist2_cluster6', 'genre_artist2_cluster7']


    # Mapping cluster values based on the modularity class
    values_for_clusters_artist1 = {var: assign_cluster_values(modularity_class_artist1, int(var.split('cluster')[-1])) for var in cluster_vars1}
    values_for_clusters_artist2 = {var: assign_cluster_values(modularity_class_artist2, int(var.split('cluster')[-1])) for var in cluster_vars2}

    
    genre_artist1_cluster0, genre_artist1_cluster1,genre_artist1_cluster2, genre_artist1_cluster3, genre_artist1_cluster4,genre_artist1_cluster5, genre_artist1_cluster6, genre_artist1_cluster7= values_for_clusters_artist1.values()

    genre_artist2_cluster0, genre_artist2_cluster1,genre_artist2_cluster2, genre_artist2_cluster3, genre_artist2_cluster4,genre_artist2_cluster5, genre_artist2_cluster6, genre_artist2_cluster7= values_for_clusters_artist2.values()

    import pandas as pd
    import copy

    # Read your CSV file into a Pandas DataFrame
    csv_file = 'Gephi Stats.csv'
    df_gephi_csv = pd.read_csv(csv_file)

    Weighted_Degree_genre_artist1=0
    Degree_genre_artist1=0
    clustering_genre_artist1=0
    eigencentrality_genre_artist1=0

    if (len(genres_artist1)>0):
        if genres_artist1[0] in df_gephi_csv['Label'].values:
            genres_row = df_gephi_csv[df_gephi_csv['Label'] == genres_artist1[0]].iloc[0]

            # Initialize variables based on the artist's gephi metrics
            Weighted_Degree_genre_artist1 = genres_row['Weighted Degree']
            Degree_genre_artist1= genres_row['Degree']
            clustering_genre_artist1= genres_row['clustering']
            eigencentrality_genre_artist1= genres_row['eigencentrality']


    Weighted_Degree_genre_artist2=0
    Degree_genre_artist2=0
    clustering_genre_artist2=0
    eigencentrality_genre_artist2=0

    if (len(genres_artist2)>0):
        if genres_artist2[0] in df_gephi_csv['Label'].values:
            genres_row = df_gephi_csv[df_gephi_csv['Label'] == genres_artist2[0]].iloc[0]

            # Initialize variables based on the artist's gephi metrics
            Weighted_Degree_genre_artist2 = genres_row['Weighted Degree']
            Degree_genre_artist2= genres_row['Degree']
            clustering_genre_artist2= genres_row['clustering']
            eigencentrality_genre_artist2= genres_row['eigencentrality']


    
    import pandas as pd
    import copy

    # Read your CSV file into a Pandas DataFrame
    csv_file = 'Gephi Stats(All Artitsts Collab).csv'
    df_gephi_artist_collab_csv = pd.read_csv(csv_file)


    clustering_artist1 = 0
    eigencentrality_artist1 = 0
    triangles_artist1=0
    Eccentricity_artist1=0
    closnesscentrality_artist1=0
    harmonicclosnesscentrality_artist1=0
    betweenesscentrality_artist1=0
    componentnumber_artist1=0
    pageranks_artist1=0
    Authority_artist1=0
    Hub_artist1=0

    if artist1 in df_gephi_artist_collab_csv['Label'].values:
        artist_row = df_gephi_artist_collab_csv[df_gephi_artist_collab_csv['Label'] == artist1].iloc[0]

        # Initialize variables based on the artist's gephi metrics
        clustering_artist1 = artist_row['clustering']
        eigencentrality_artist1 = artist_row['eigencentrality']
        triangles_artist1 = artist_row['triangles']
        eccentricity_artist1 = artist_row['Eccentricity']
        closenesscentrality_artist1 = artist_row['closnesscentrality']
        harmonic_closenesscentrality_artist1 = artist_row['harmonicclosnesscentrality']
        betweennesscentrality_artist1 = artist_row['betweenesscentrality']
        component_number_artist1 = artist_row['componentnumber']
        pagerank_artist1 = artist_row['pageranks']
        authority_artist1 = artist_row['Authority']
        hub_artist1 = artist_row['Hub']

    
    clustering_artist2 = 0
    eigencentrality_artist2 = 0
    triangles_artist2=0
    Eccentricity_artist2=0
    closnesscentrality_artist2=0
    harmonicclosnesscentrality_artist2=0
    betweenesscentrality_artist2=0
    componentnumber_artist2=0
    pageranks_artist2=0
    Authority_artist2=0
    Hub_artist2=0

    if artist2 in df_gephi_artist_collab_csv['Label'].values:
        artist_row = df_gephi_artist_collab_csv[df_gephi_artist_collab_csv['Label'] == artist2].iloc[0]

        # Initialize variables based on the artist's gephi metrics
        clustering_artist2 = artist_row['clustering']
        eigencentrality_artist2 = artist_row['eigencentrality']
        triangles_artist2 = artist_row['triangles']
        eccentricity_artist2 = artist_row['Eccentricity']
        closenesscentrality_artist2 = artist_row['closnesscentrality']
        harmonic_closenesscentrality_artist2 = artist_row['harmonicclosnesscentrality']
        betweennesscentrality_artist2 = artist_row['betweenesscentrality']
        component_number_artist2 = artist_row['componentnumber']
        pagerank_artist2 = artist_row['pageranks']
        authority_artist2 = artist_row['Authority']
        hub_artist2 = artist_row['Hub']

    l = [track_number, duration_ms, key, mode, time_signature, acousticness, danceability, energy, instrumentalness,       liveness, loudness, speechiness, valence, tempo, followers_artist1, popularity_artist1, followers_artist2,       popularity_artist2, artist1_num_available_markets,       artist2_num_available_markets, release_date_year,       release_date_month,release_date_day,       Weighted_Degree_genre_artist1, Degree_genre_artist1,       clustering_genre_artist1, eigencentrality_genre_artist1,       Weighted_Degree_genre_artist2, Degree_genre_artist2,       clustering_genre_artist2, eigencentrality_genre_artist2,       clustering_artist1, eigencentrality_artist1, triangles_artist1,       Eccentricity_artist1, closnesscentrality_artist1,       harmonicclosnesscentrality_artist1, betweenesscentrality_artist1,       componentnumber_artist1, pageranks_artist1, Authority_artist1,       Hub_artist1, clustering_artist2, eigencentrality_artist2,       triangles_artist2, Eccentricity_artist2,       closnesscentrality_artist2,harmonicclosnesscentrality_artist2,       betweenesscentrality_artist2, componentnumber_artist2,       pageranks_artist2, Authority_artist2, Hub_artist2     ,  genre_artist1_cluster0, genre_artist1_cluster1,       genre_artist1_cluster2,genre_artist1_cluster3,       genre_artist1_cluster4,genre_artist1_cluster5,       genre_artist1_cluster6,genre_artist1_cluster7,       genre_artist2_cluster0,genre_artist2_cluster1,       genre_artist2_cluster2,genre_artist2_cluster3,       genre_artist2_cluster4,genre_artist2_cluster5,       genre_artist2_cluster6,genre_artist2_cluster7, explicit_True]#,artist1,artist2]
    
    X.loc[len(X)] = l
    song_popularity_index = loaded_model.predict(pd.DataFrame(X.iloc[0]).T)
    if song_popularity_index[0] == 2:
        song_popularity="High"
    elif song_popularity_index[0] == 1:
        song_popularity="Average"
    else:
        song_popularity = "Low"
    return song_popularity
    
    
# acousticness = 0.276
# danceability = 0.639
# energy = 0.536
# instrumentalness = 0
# liveness = 0.0846
# loudness = -6.328
# speechiness = 0.0963
# valence = 0.265
# tempo = 80.902
# artist1="Ed Sheeran"
# artist2 = "Justin Beiber"
# print("Song Popularity = ",prediction(artist1,artist2,acousticness,danceability,energy,instrumentalness,liveness,loudness,speechiness, valence, tempo)    )


# Creating list from df_artist dataframe for artist search button:
df_artists=pd.read_csv("Music dataset/Artists/spotify_artists_info_complete.csv", sep="\t")
df_artists.drop("image_url",axis=1,inplace=True)
df_artists.rename(columns={"name":"artist_name"},inplace=True)
df_artists.head()
all_artists = df_artists['artist_name'].tolist()


# Streamlit app
st.set_page_config(layout="centered")


# Add a background image using custom HTML and CSS
page_bg_img = '''
<style>
.stApp {
  background-image: url("https://img.freepik.com/premium-photo/headphones_522560-13672.jpg?size=626&ext=jpg&ga=GA1.1.1826414947.1699660800&semt=ais");
  background-size: cover;
  @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css');
}
.stText {
  color: white;  /* Set text color to white for st.write */
}

.info-icon {
    color: #4CAF50;  /* Set color for information icon */
    cursor: pointer;
}
.sidebar .sidebar-content {
                width: 105px;
}
'''

st.markdown(page_bg_img, unsafe_allow_html=True)


st.title("Song Collaboration Popularity Prediction")
    
# Input form
artist1 = st.selectbox("Select Artist 1", all_artists)
artist2 = st.selectbox("Select Artist 2", all_artists)

st.write("### Song Features:")

# Use st.columns to create two columns
col1, col2 = st.columns(2)

# Add horizontal space between columns
col1.write("<style>div.row-widget.stHorizontal > div{margin-right: 2em;}</style>", unsafe_allow_html=True)


# Function to display information on hover
def show_info(info_text):
    st.info(info_text)
    
# with col1:
acousticness = st.slider("**Acousticness**",min_value=0.0,max_value=1.0,value=0.5,help="A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.")
danceability=st.slider("**Danceability**", 0.0, 1.0, 0.5,help="Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable")
energy=st.slider("**Energy**",help="Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.", min_value=0.0, max_value=1.0, value=0.5)
instrumentalness = st.slider("**Instrumentalness**", 0.0, 1.0, 0.5,help=" Predicts whether a track contains no vocals. 'Ooh' and 'aah' sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly 'vocal'. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.")
st.markdown("")  # Add a blank line after the slider
tempo=st.slider("**Tempo**", 0.0, 250.0, 100.0,help="The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.")
    
# with col2:     
liveness = st.slider("**Liveness**",0.0, 1.0, 0.5,help="Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live")
loudness = st.slider("**Loudness**", -10.0, 10.0, 0.0,help=" The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.")
speechiness = st.slider("**Speechiness**",0.0, 1.0, 0.5,help= "detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.")
valence = st.slider("**Valence**",  0.0, 1.0, 0.5,help="A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).")
    

# Run prediction on button click
if st.button("Predict"):
    result = prediction(artist1, artist2, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo)
    st.success(f"Predicted Song Popularity: {result}")

# Stop the application if user clicks on the "Stop" button
if st.button("Stop"):
    st.balloons()
