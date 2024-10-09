import streamlit as st
import pickle
import pandas as pd
import requests
import json

data = pd.DataFrame(pickle.load(open('data.pkl', 'rb')))

movie_similarity = pickle.load(open('similarity.pkl', 'rb'))

def get_recommendation(movie_name):
  movies=sorted(list(enumerate(movie_similarity[data[data['title_y']==movie_name].index[0]])) ,reverse=True,key=lambda x : x[1])
  indices=[]
  for i in range(1,6):
    indices.append(list(data.loc[movies[i][0],['title_y','imdb_id']]))
  return indices

def get_url(id):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/'
  }
  response = requests.get('http://www.omdbapi.com/?i={}&apikey=604c0287'.format(id), headers=headers)
  return json.loads(response.text)['Poster']

st.title('Movie Recommendation')

option = st.selectbox('Select Movie',
                      data['title_y'].tolist())


if st.button("Recommend"):
  movie_name = option
  info = get_recommendation(movie_name)
  col = st.columns(5)
  for i in zip(col,info):
    with i[0]:
      st.header(i[1][0])
      st.image(get_url(i[1][1]))
      # st.write(i[1][1])