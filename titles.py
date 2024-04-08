import googleapiclient.discovery  # Import the Google API client library
import re  # Import the regular expression module
import unicodedata  # Import the unicodedata module to handle Unicode characters

# Set up the YouTube API parameters
api_service_name = 'youtube'
api_version = 'v3'
DEVELOPER_KEY = 'AIzaSyBI_hPBMA6J98wsIyDShyk1I4uzhDNh02k'  # Replace with your actual developer key
#Link to get developer key: https://blog.hubspot.com/website/how-to-get-youtube-api-key

#YouTube URL of playlist:  https://www.youtube.com/watch?v=OW6yRfdrfgU&list=PL13f76aevJUXNvJU3Bbtymq3btS6TaBma
playlist_id = 'PL13f76aevJUXNvJU3Bbtymq3btS6TaBma'  # Replace with your playlist ID

# Build the YouTube API client
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

# Retrieve the list of videos in the playlist
request = youtube.playlistItems().list(
    part='snippet',  # Specify that we want to retrieve the 'snippet' part of each video
    playlistId=playlist_id,  # Specify the playlist ID
    maxResults=50,  # Increase maxResults to fetch more items per page, up to 50
)

# Execute the API request
response = request.execute()
lst = []  # Initialize an empty list to store video titles

# Loop through each page of results until there are no more pages
while response.get('items'):
    # Loop through each video item in the response
    for item in response['items']:
        title = item['snippet']['title']  # Get the title of the video from the 'snippet' part

        # Remove Unicode characters using unicodedata.normalize
        clean_title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('utf-8')

        # Split the title by '|', '(', or '-' to extract relevant parts
        parts = [part.strip() for part in re.split(r'\||\(|\)', clean_title) if part.strip()]

        # Append the relevant parts to the list
        if len(parts) >= 1:
            lst.append(parts[0])
        else:
            lst.append(None)

    # Check if there's another page of results
    if 'nextPageToken' in response:
        # Make another API request for the next page of results
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=response['nextPageToken']  # Use the nextPageToken from the current response
        )
        response = request.execute()  # Execute the API request for the next page
    else:
        break  # Break out of the loop if there are no more pages

print(lst)  # Print the list of video titles



### If you need title for 1 page of playlist only

# import googleapiclient.discovery  # Import the Google API client library
# import re  # Import the regular expression module
# import unicodedata  # Import the unicodedata module to handle Unicode characters

# # Set up the YouTube API parameters
# api_service_name = 'youtube'
# api_version = 'v3'
# DEVELOPER_KEY = ''  # Replace with your actual developer key
# playlist_id = ''  # Replace with your playlist ID

# # Build the YouTube API client
# youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

# # Retrieve the list of videos in the playlist (first page only)
# request = youtube.playlistItems().list(
#     part='snippet',  # Specify that we want to retrieve the 'snippet' part of each video
#     playlistId=playlist_id,  # Specify the playlist ID
#     maxResults=50,  # Increase maxResults to fetch more items per page, up to 50
# )

# # Execute the API request for the first page of results
# response = request.execute()
# lst = []  # Initialize an empty list to store video titles

# # Loop through each video item in the response
# for item in response['items']:
#     title = item['snippet']['title']  # Get the title of the video from the 'snippet' part

#     # Remove Unicode characters using unicodedata.normalize
#     clean_title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('utf-8')

#     # Split the title by '|', '(', or '-' to extract relevant parts
#     parts = [part.strip() for part in re.split(r'\||\(|\)', clean_title) if part.strip()]

#     # Append the relevant parts to the list
#     if len(parts) >= 1:
#         lst.append(parts[0])
#     else:
#         lst.append(None)

# print(lst)  # Print the list of video titles from the first page of results

