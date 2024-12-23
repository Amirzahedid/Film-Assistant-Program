import streamlit as st
from backend import fetch_movie_data_omdb, fetch_movie_data_tmdb, summarize_movie_data, answer_question, sanitize_input

# Set page configuration
st.set_page_config(page_title="Film Assistant", page_icon="🎬", layout="wide")

# Apply custom CSS for styling
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #ece9e6, #ffffff);
        font-family: 'Arial', sans-serif;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        margin: 10px 0;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stExpander {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .stSidebar .sidebar-content {
        background-color: #343a40;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .stSidebar .sidebar-content .stButton>button {
        background-color: #6c757d;
        color: white;
        border: none;
        padding: 10px 20px;
        margin: 10px 0;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .stSidebar .sidebar-content .stButton>button:hover {
        background-color: #5a6268;
    }
    .movie-card {
        background: #fff;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .movie-card img {
        border-radius: 10px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('Film Assistant Program 🎬')

# Sidebar for inputs
st.sidebar.header('Movie Selection')
movie_name = sanitize_input(st.sidebar.text_input('Enter the movie name:'))

# Initialize session state variables
if 'movie_data1' not in st.session_state:
    st.session_state.movie_data1 = None
if 'movie_data2' not in st.session_state:
    st.session_state.movie_data2 = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'guide_displayed' not in st.session_state:
    st.session_state.guide_displayed = True

# Fetch movie information
if st.sidebar.button('Fetch Movie Information'):
    st.session_state.movie_data1 = None
    st.session_state.movie_data2 = None
    st.session_state.summary = None
    with st.spinner('Fetching data...'):
        try:
            movie_data1 = fetch_movie_data_tmdb(movie_name)
            movie_data2 = fetch_movie_data_omdb(movie_name)
            if movie_data1:
                st.session_state.movie_data1 = movie_data1
                st.session_state.movie_data2 = movie_data2
                plot = movie_data1.get('overview', '') + movie_data2.get('Plot', '')
                title = movie_data1.get("original_title", '')
                st.session_state.summary = summarize_movie_data(plot, title)
                st.success('Movie information fetched!')
                st.session_state.guide_displayed = False
            else:
                st.error('Movie not found.')
        except Exception as e:
            st.error(f"Error fetching movie information: {e}")

# Display user guide
if st.session_state.guide_displayed:
    st.markdown("""
    ### How to Use This Website:

    1. **Select a Movie**
                
    2. **Fetch Movie Information**
                
    3. **View Movie Summary and Details**
                
    4. **Ask Questions**

    """)

# Display movie summary
if st.session_state.summary:
    st.markdown(f"## **{st.session_state.movie_data1.get('title', 'N/A')}**")
    st.markdown(f"### Summary")
    st.markdown(f"**{st.session_state.summary}**")

# Section for asking questions
st.sidebar.header('Questions about the Movie')
question = sanitize_input(st.sidebar.text_input('Ask a question about the movie:'))

if st.sidebar.button('Get Answer'):
    if st.session_state.movie_data1 or st.session_state.movie_data2:
        with st.spinner('Generating answer...'):
            try:
                answer = answer_question(question, st.session_state.movie_data1, st.session_state.movie_data2)
                st.success('Answer generated!')
                st.header('Answer')
                st.markdown(f"**{answer}**")
            except Exception as e:
                st.error(f"Error generating answer: {e}")
    else:
        st.error('Please fetch the movie information first.')

# Display movie information in a card
if st.session_state.movie_data1:
    if 'poster_path' in st.session_state.movie_data1:
        poster_url = f"https://image.tmdb.org/t/p/w500{st.session_state.movie_data1['poster_path']}"
        st.image(poster_url, caption="Movie Poster")
    st.markdown(f"### **{st.session_state.movie_data1.get('title', 'N/A')}**")
    st.markdown(f"**Release Date:** {st.session_state.movie_data1.get('release_date', 'N/A')}")
    st.markdown(f"**Rating:** {st.session_state.movie_data1.get('vote_average', 'N/A')}")
    st.markdown(f"**Genres:** {', '.join([genre['name'] for genre in st.session_state.movie_data1.get('genres', [])])}")
    st.markdown(f"**Overview:** {st.session_state.movie_data1.get('overview', 'N/A')}")

    with st.expander("Movie Details"):
        st.subheader("Movie Information")
        st.json(st.session_state.movie_data2)
