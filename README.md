# Music Recommendation System

## Overview

This project is a content-based music recommendation system that suggests songs based on an uploaded audio file. The system extracts features from the uploaded file, finds similar songs from the FMA dataset using a KNN model, and fetches additional metadata from the Spotify API.

## Project Structure

The project is divided into the following components:

- **Machine Learning Model (Flask Server)** – Extracts audio features, performs recommendations.
- **Backend (Node.js Server)** – Handles API requests, communicates with the Flask server, fetches metadata from Spotify.
- **Frontend (ReactJS)** – Provides the user interface for uploading audio and displaying recommendations.
- **Database (MongoDB)** – Caches fetched metadata.

## Installation and Setup

### 1. Setting Up the Machine Learning Model

Navigate to the `MLmodel` directory and ensure:

- A virtual environment is activated.
- Python version is **3.11 or below**.
- All required libraries are installed using:
  ```sh
  pip install -r requirements.txt
  ```

#### Preprocessing the Dataset

Run the following Python scripts in order to preprocess the dataset:

```sh
python merge_csv.py
python clean.py
python encoding.py
python tfidf.py
python normalize.py
```

Once preprocessing is complete, the dataset is ready for training.

#### Training the Model

Run the following command to train the KNN model:

```sh
python knn.py
```

#### Running the Flask Server

Once the model is trained, start the Flask server:

```sh
python app.py
```

The Flask server runs on **port 7000** and handles file uploads and recommendations.

### 2. Setting Up the Node.js Server

In another Tab navigate to the `server` directory and install dependencies:

```sh
cd server
npm i
```

Start the server:

```sh
npm start
```

The Node.js server runs on **port 5000**.

### 3. Setting Up the Frontend

In another Tab navigate to the `client` directory, install dependencies, and start the client:

```sh
cd client
npm i
npm start
```

The frontend runs on **port 3000** and will open in the browser automatically.

## Environment Variables

The project requires `.env` files inside the **ML model** and **server** directories. These environment variables should be configured according to your system and credentials before running the project.

## Running the Application

1. Install dependencies in the ML model (`pip install -r requirements.txt`).
2. Start the **Flask server** (`python find-app.py` on port **7000**).
3. Start the **Node.js server** (`npm start` inside `server/` on port **5000**).
4. Start the **React frontend** (`npm start` inside `client/` on port **3000**).
5. Open the web application in your browser, upload an audio file, and receive music recommendations.

## Workflow

1. The user uploads an audio file via the frontend.
2. The file is sent to the Node.js backend via API calls.
3. Node.js temporarily saves the file and forwards it to the Flask server.
4. Flask extracts features, finds similar songs using KNN, and returns song indices and track titles from the FMA dataset.
5. Node.js queries the Spotify API to fetch additional metadata on the recommended tracks.
6. The combined recommendations are sent back to the frontend and displayed to the user.

## Notes

- Ensure that all dependencies are installed before running the project.
- The environment variables must be correctly set up inside the `MLmodel` and `server` directories.
- Flask runs on **port 7000**, Node.js on **port 5000**, and React on **port 3000**.

Enjoy using the music recommendation system!
