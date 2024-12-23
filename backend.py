import requests
from transformers import pipeline
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMRequestsChain, LLMChain
from langchain_openai.llms import OpenAI
from decouple import config

import re
import urllib.parse


import openai
import numpy as np

# API-Keys
OMDB_API_KEY = config('OMDB_API_KEY')
TMDB_API_KEY = config('TMDB_API_KEY')

# Function to find movie name from search results
# def find_movie_name(input_text):
#     try:
#         template = """
#         Extract the movie name from the following search result or say "not found" if the information is not available.
#         Query: {input}
#         Search Result: {requests_result}
#         """

#         prompt = PromptTemplate(
#             input_variables=["input", "requests_result"],
#             template=template,
#         )

#         llm = OpenAI()
#         chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=prompt))

#         search_url = "https://www.google.com/search?q=" + input_text.replace(" ", "+")
#         inputs = {
#             "input": input_text,
#             "url": search_url,
#         }

#         movie_name = chain.invoke(inputs)
#         return movie_name['output']
#     except Exception as e:
#         print(f"Failed to find movie name: {e}")
#         return "not found"



def sanitize_input(input_text):
    return re.sub(r'[^\w\s]', '', input_text)

# Function to fetch movie data from TMDB
def fetch_movie_data_tmdb(movie_name):
    try:
        encoded_movie_name = urllib.parse.quote(movie_name)
        search_url = f"https://api.themoviedb.org/3/search/movie?query={encoded_movie_name}&api_key={TMDB_API_KEY}"
        search_response = requests.get(search_url)
        search_response.raise_for_status()

        search_results = search_response.json()
        if search_results['results']:
            movie_id = search_results['results'][0]['id']
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
            details_response = requests.get(details_url)
            details_response.raise_for_status()

            return details_response.json()
        else:
            print(f"No results found on TMDB for: {movie_name}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching TMDB data: {e}")
        return None

# Function to fetch movie data from OMDB
def fetch_movie_data_omdb(movie_name):
    try:
        encoded_movie_name = urllib.parse.quote(movie_name)
        url = f"https://www.omdbapi.com/?t={encoded_movie_name}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()

        movie_data = response.json()
        if movie_data.get('Response') == 'True':
            return movie_data
        else:
            print(f"Error: {movie_data.get('Error', 'Unknown error')}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching OMDB data: {e}")
        return None

# Function to answer a question based on movie data
def answer_question(question, movie_data1, movie_data2):
    try:
        client = openai.Client()

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Movie data: {movie_data1} and {movie_data2}\n\nQuestion: {question}\nAnswer:"}
            ],
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.9,
        )

        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        print(f"Error answering question: {e}")
        return None

# Function to summarize data
def summarize_data(plot):
    try:
        client = openai.Client()

        chat_completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following text:\n\n{plot}\n\nSummary:"}
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.9,
        )

        summary = chat_completion.choices[0].message.content
        return summary
    except Exception as e:
        print(f"Error summarizing data: {e}")
        return None

# Function to summarize movie data using LLama
def summarize_movie_data(plot, title):
    try:
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        model_name ="C:\Personal\llama-2-7b-chat.Q2_K.gguf" #"TheBloke/Llama-2-7B-Chat-GGUF" 
        llm = CTransformers(model=model_name, max_tokens=5000, callback_manager=callback_manager, verbose=True)
        
        template = """
        This information is about the movie {title} with this review: {plot}. Give a summary of the movie so that the reader will be interested in watching the movie.
        Your Response:
        """
        
        prompt = PromptTemplate(
            input_variables=["title", "plot"],
            template=template,
        )

        response = llm.invoke(prompt.format(title=title, plot=plot))
        return summarize_data(response)
    except Exception as e:
        print(f"Error summarizing movie data: {e}")
        return None
    
#Function to summarize movie data using HuggingFace
# def summarize_movie_data(plot, title):
#     # Initialize the summarization pipeline
#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

#     # Generate the summary
#     summary_list = summarizer(plot, max_length=200, min_length=10, do_sample=False)

#     # Extract the summary text
#     summary = summary_list[0]['summary_text']
#     return summary
