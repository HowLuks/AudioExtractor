from flask import Flask, request, jsonify
from moviepy import VideoFileClip
import gdown
import uuid
import traceback

app = Flask(__name__)

@app.route("/extrair-audio", methods=["POST"])
def extrair_audio():
    data = request.get_json()
    file_id = data.get("id")
    if not file_id:
        return jsonify({"erro": "ID do arquivo não fornecido"}), 400

    try:
        video_id = str(uuid.uuid4())
        video_path = f"/tmp/{video_id}.mp4"
        audio_path = f"/tmp/{video_id}.mp3"

        # Baixa o vídeo pelo ID
        gdown.download(f"https://drive.google.com/uc?id={file_id}", video_path, quiet=False)

        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)
        clip.close()

        return jsonify({"mensagem": "Áudio extraído com sucesso!", "arquivo": audio_path})
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        return jsonify({"erro": str(e), "traceback": tb}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
