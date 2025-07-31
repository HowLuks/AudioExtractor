from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip
import gdown
import uuid
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Servidor rodando!"

@app.route("/extrair-audio", methods=["POST"])
def extrair_audio():
    data = request.get_json()
    link = data.get("link")

    try:
        if "id=" in link:
            file_id = link.split("id=")[-1]
        elif "/d/" in link:
            file_id = link.split("/d/")[-1].split("/")[0]
        else:
            return jsonify({"erro": "Link inválido"}), 400

        video_id = str(uuid.uuid4())
        video_path = f"{video_id}.mp4"
        audio_path = f"{video_id}.mp3"

        gdown.download(f"https://drive.google.com/uc?id={file_id}", video_path, quiet=False)

        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)
        clip.close()

        return jsonify({"mensagem": "Áudio extraído com sucesso", "arquivo": audio_path})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
