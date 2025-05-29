from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/bestmove', methods=['POST'])
def bestmove():
    data = request.json
    fen = data.get('fen')
    if not fen:
        return jsonify({'error': 'Missing FEN'}), 400

    try:
        engine = subprocess.Popen(
            ["./stockfish"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        engine.stdin.write(f"position fen {fen}\n")
        engine.stdin.write("go movetime 1000\n")
        engine.stdin.flush()

        while True:
            line = engine.stdout.readline()
            if line.startswith("bestmove"):
                move = line.split()[1]
                break
        engine.kill()
        return jsonify({'bestmove': move})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

