import streamlit as st
import pandas as pd
from pytube import YouTube
import googleapiclient.discovery
import googleapiclient.errors
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os 
from textblob import TextBlob
from deep_translator import GoogleTranslator
import regex as re 
import seaborn as sns

def get_path(path):
  path = st.text_input('Enter URL of Mann ki Baat youtube video')
  return path


api_key = os.getenv(DEVELOPER_KEY) # get google developer key for translating sentences 
def get_youtube_comments(path, max_results=500):
    load_dotenv()
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    query = parse_qs(urlparse(path).query)
    video_id = query["v"][0]

    comments = []

    # Set the initial page token to None
    page_token = None

    # Continue fetching comments until the desired number is reached or no more comments are available
    while len(comments) < max_results and (not page_token or 'nextPageToken' in response):
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(100, max_results - len(comments)),  # Limit to 100 comments per request
            pageToken=page_token  # Use the page token for pagination
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                # comment['publishedAt'],
                # comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])

        # Update the page token for the next request
        page_token = response.get('nextPageToken')

    df = pd.DataFrame(comments, columns=['author', 'like_count', 'comment'])
    df.to_csv('sentiment/comments.csv',index=False) #add path for comments.csv
    return df

def sentiment(df):
  df = pd.read_csv('sentiment/comments.csv') #add path for comments.csv

  def preprocess_text(text):
      print("in preprocessing")
      text=str.lower(text)
      emoji_pattern = re.compile("["
          u"\U0001F600-\U0001F64F"  # emoticons
          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
          u"\U0001F680-\U0001F6FF"  # transport & map symbols
          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)
      text=emoji_pattern.sub(r'', text)
      text=re.sub('❤','emoji replaced by text',text)
      text=emoji_pattern.sub(r'', text)
      # Remove HTML tags
      text = re.sub(r'<.*?>', '', text)
      return text


  # Function to translate Hindi text to English using Google Translate
  def translate_to_english(text):
      print("in translation")
      if not text.startswith(('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')):
          translated = GoogleTranslator(source='hindi', target='en').translate(text)
          # print(translated)
          return translated
      return text

  # Function to perform sentiment analysis using TextBlob
  def analyze_sentiment(text):
      print("in sentiment")
      analysis = TextBlob(text)
      polarity = analysis.sentiment.polarity
      
      negative_words = ["bardab", "feku", "chand", "dislike", "bad",'ghatiya','Ghatiya',"Dislike",'dislike','anpor']
      
      for word in negative_words:
          if word in text:
              polarity -= 0.2  # You can adjust this value based on the impact you want

      if polarity > 0:
          return 'Positive'
      elif polarity < 0:
          return 'Negative'
      else:
          return 'Neutral'
   
  # Apply sentiment analysis to the DataFrame
  df['clean_comment'] =df['comment'].apply(preprocess_text)  # Preprocess text (remove emojis and HTML tags)
  df['clean_comment'] =df['clean_comment'].apply(translate_to_english) 
  df['sentiment'] = df['clean_comment'].apply(analyze_sentiment)
  # sns.countplot(data=df,x=df['sentiment'])
  return df 


def main():
  path=st.text_input('Enter URL of Mann ki Baat youtube video')
  col1, col2, col3 = st.columns(3)

  # Button for playing the video
  if col1.button("Play"):
      st.video(path)

  # Button for displaying comments:
  with st.spinner('Processing...'):
    if col2.button("Comments"):
        comments = get_youtube_comments(path)
        st.write(comments)

  # Button for sentiment analysis
  with st.spinner('Processing...'):
    if col3.button("Sentiment"):
        comment = get_youtube_comments(path)
        comments = sentiment(comment)
        st.write(comments)
		
if __name__ == '__main__':
	main()