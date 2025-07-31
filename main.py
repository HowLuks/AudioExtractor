from flask import Flask, request, jsonify
import subprocess
import gdown
import uuid
import os
import traceback

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Servidor está online!"

@app.route("/extrair-audio", methods=["POST"])
def extrair_audio():
    data = request.get_json()
    file_id = data.get("id")

    if not file_id:
        return jsonify({"erro": "ID do arquivo não fornecido"}), 400

    try:
        # Cria caminhos únicos para vídeo e áudio
        video_id = str(uuid.uuid4())
        video_path = f"/tmp/{video_id}.mp4"
        audio_path = f"/tmp/{video_id}.mp3"

        # Faz download do vídeo do Google Drive
        gdown.download(f"https://drive.google.com/uc?id={file_id}", video_path, quiet=False)

        # Extrai o áudio usando ffmpeg via subprocess
        command = [
            "ffmpeg", "-i", video_path,
            "-vn", "-acodec", "libmp3lame",
            "-ab", "192k", "-ar", "44100", "-y",
            audio_path
        ]
        subprocess.run(command, check=True)

        return jsonify({
            "mensagem": "Áudio extraído com sucesso!",
            "arquivo": audio_path
        })

    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        return jsonify({
            "erro": str(e),
            "traceback": tb
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
