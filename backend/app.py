from flask import Flask, request, jsonify, render_template, send_from_directory
from .game import TicTacToe
from .ai import minimax
import os

app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend')),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
)

game = TicTacToe()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset_game():
    global game
    game = TicTacToe()
    return jsonify({"board": game.board})

@app.route("/move", methods=["POST"])
def make_move():
    global game
    data = request.json
    square = data.get("square")
    player = data.get("player")

    if not game.make_move(square, player):
        return jsonify({"error": "Invalid move"}), 400

    resp = {"board": game.board}
    if game.current_winner == player:
        resp["winner"] = player
        return jsonify(resp)

    # AI's turn
    ai_move = minimax(game, 'O')['position']
    game.make_move(ai_move, 'O')
    resp["ai_move"] = ai_move

    if game.current_winner == 'O':
        resp["winner"] = 'O'

    return jsonify(resp)

@app.route("/board", methods=["GET"])
def get_board():
    return jsonify({"board": game.board, "winner": game.current_winner})

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
