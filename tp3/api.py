# api.py
from flask import Flask, jsonify
from google.cloud import storage
import os

app = Flask(__name__)

@app.route('/')
def home():
    """Route racine - Page d'accueil"""
    return jsonify({
        "status": "ok",
        "message": "Cloud Run Backend Service",
        "endpoints": {
            "/": "Cette page",
            "/list": "Liste les fichiers du bucket Cloud Storage"
        }
    })

@app.route('/list')
def list_files():
    """Liste les fichiers du bucket Cloud Storage"""
    try:
        bucket_name = os.environ.get('BUCKET_NAME')
        
        if not bucket_name:
            return jsonify({
                "error": "BUCKET_NAME environment variable not set"
            }), 500
        
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        
        blobs = bucket.list_blobs()
        files = [blob.name for blob in blobs]
        
        return jsonify({
            "bucket": bucket_name,
            "files": files,
            "count": len(files)
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/health')
def health():
    """Vérification de l'état de santé"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))