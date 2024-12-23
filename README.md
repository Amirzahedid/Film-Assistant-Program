# Film Assistant Program

## Overview

The **Film Assistant Program** is a web application built using **Streamlit** to provide users with information about movies. It fetches movie details from **TMDB** and **OMDB** APIs, generates summaries, and answers user questions using **large language models (LLMs)**. This tool is perfect for movie enthusiasts looking for a quick and interactive way to explore films.

## Features

1. **Movie Information Fetching**:

   - Fetches data about movies from two APIs: TMDB and OMDB.
   - Displays movie details like title, release date, genres, rating, and an overview.

2. **Movie Summarization**:

   - Generates an engaging summary of the movie using AI-based models (e.g., GPT or LLaMA).

3. **Question-Answering**:

   - Allows users to ask questions about the movie, with answers generated based on available data.

4. **Interactive User Interface**:

   - Easy-to-use sidebar for inputs.
   - Beautifully styled interface with custom CSS.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Pip (Python package manager)

Additionally, you need API keys for the following services:

- **OpenAI API**: Required for GPT-based summarization and Q&A.
- **Huggingface API**: Required if using models hosted on Huggingface.

These API keys should be configured in your system environment or in a `.env` file as explained below.

### Steps

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd film-assistant
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys:

   - Create a `.env` file in the root directory.
   - Add your TMDB, OMDB, OpenAI, and Huggingface API keys:
     ```env
     TMDB_API_KEY=your_tmdb_api_key
     OMDB_API_KEY=your_omdb_api_key
     OPENAI_API_KEY=your_openai_api_key
     HUGGINGFACE_API_KEY=your_huggingface_api_key
     ```

4. Configure the model:

   - Download the LLaMA 2 model from an official source (e.g., Meta AI).
   - Save the model file in a local directory (e.g., `C:\Personal\llama-2-7b-chat.Q2_K.gguf`).
   - Update the model path in `backend.py`:
     ```python
     model_name = "path/to/your/llama-2-model.Q2_K.gguf"
     ```
   - Alternatively, use the `.env` file to store the path:
     ```env
     MODEL_PATH=path/to/your/llama-2-model.Q2_K.gguf
     ```

5. Run the application:

   ```bash
   streamlit run app.py
   ```

6. Access the app in your browser at `http://localhost:8501`.

## File Structure

```
film-assistant/
|
├── app.py          # Main application file (Streamlit UI).
├── backend.py      # Backend logic for API calls and data processing.
├── requirements.txt# List of Python dependencies.
└── .env.example    # Example of environment variables.
```

## Usage

### 1. Fetch Movie Information

- Enter a movie name in the sidebar and click **Fetch Movie Information**.
- The application fetches data from TMDB and OMDB and displays detailed information, including:
  - Title
  - Release Date
  - Genres
  - Rating
  - Overview

### 2. View Movie Summary

- After fetching movie information, the app generates a summary using AI.
- The summary is displayed below the movie details.

### 3. Ask Questions

- Enter a question in the sidebar (e.g., "What is the genre of the movie?") and click **Get Answer**.
- The app generates an AI-powered answer based on the fetched movie data.

## Security Features

- **Input Sanitization**: All user inputs are sanitized to prevent injection attacks.
- **Environment Variables**: API keys are securely stored in `.env` file.
- **Error Handling**: Graceful handling of API errors and user-friendly error messages.

## Technologies Used

- **Frontend**: Streamlit for UI.
- **Backend**: Python for API calls and data processing.
- **APIs**:
  - TMDB (The Movie Database)
  - OMDB (Open Movie Database)
  - OpenAI API
  - Huggingface API
- **AI Models**: GPT, LLaMA for summarization and Q&A.

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or suggestions, please contact Amir Zahedidarehshoori at [amirzahedi01@gmail.com](mailto:amirzahedi01@gmail.com).

