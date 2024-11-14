from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return 'YouTube Video Downloader API'

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')

    if not video_url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Create yt-dlp options to fetch the video
        ydl_opts = {
            'quiet': True,
            'format': 'best',
            'noplaylist': True,  # Avoid playlist downloads
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            download_link = info_dict.get('url', None)  # Get direct video URL

            if not download_link:
                return jsonify({"error": "Failed to fetch download link"}), 500

            return jsonify({"downloadLink": download_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
