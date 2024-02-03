import os

from flask import request, jsonify, send_from_directory
from app import app
from compiler import main as compiler


@app.route('/api/compile', methods=['POST'])
def compile_code():
    code = request.json.get('code', '')
    try:
        data = compiler.process_command('interpret', source_code=code)
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main(path):
    full_path = os.path.join(app.static_folder, path)
    if path != "" and os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
