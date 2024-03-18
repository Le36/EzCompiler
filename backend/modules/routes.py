import os

from app import app
from flask import request, jsonify, send_from_directory, send_file

from compiler import main as compiler


@app.route('/download/executable')
def download_executable():
    executable_path = os.path.join(app.root_path, 'a.out')

    if not os.path.exists(executable_path):
        return jsonify({"error": "Executable file not found."}), 404

    return send_file(executable_path, as_attachment=True, download_name="executable.out",
                     mimetype='application/octet-stream')


@app.route('/api/compile', methods=['POST'])
def compile_code():
    code = request.json.get('code', '')
    try:
        data = compiler.process_command('interpret', source_code=code)
        return jsonify(data)
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
