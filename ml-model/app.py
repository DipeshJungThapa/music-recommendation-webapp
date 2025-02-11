from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from recommend import save_uploaded_file, process_uploaded_file, load_and_preprocess_data, get_song_recommendations

app = Flask(__name__)
CORS(app)

load_dotenv()

SAVE_DIRECTORY = os.getenv('AUDIO_DIRECTORY', 'uploads')
TF_IDF_PATH = os.getenv('TF_IDF_PATH')
KNN_MODEL_PATH = os.getenv('MODEL_PATH')
PCA_MODEL_PATH = os.getenv('PCA_PATH')
MERGED_CLEANED_PATH = os.getenv('MERGED_CLEANED_PATH')


os.makedirs(SAVE_DIRECTORY, exist_ok=True)


app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  


@app.route('/recommend', methods=['POST'])
def recommend():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        
        file_path = save_uploaded_file(file, SAVE_DIRECTORY)
        if not os.path.exists(file_path):
            return jsonify({"error": f"File was not saved at {file_path}."}), 500

        
        combined_data = process_uploaded_file(file_path)
        df_dataset, df_with_tfidf = load_and_preprocess_data(combined_data, MERGED_CLEANED_PATH, TF_IDF_PATH)
        recommended_tracks = get_song_recommendations(df_with_tfidf, df_dataset, KNN_MODEL_PATH, PCA_MODEL_PATH)

        
        os.remove(file_path)

        return jsonify({"recommended_tracks": recommended_tracks})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
