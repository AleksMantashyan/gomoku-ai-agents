from flask import Flask, jsonify, request, render_template
from Board import Board
from RandomAgent import RandomAgent
from AlphaBetaAgent import AlphaBetaAgent
from HeuristicMinimaxAgent import MinimaxAgent

app = Flask(__name__)

board = Board()
current_player = 1
last_move = None
winner = None

PROXIMITY = 2

# type: "human", "random", "alphabeta", "minimax"
player_types = {
    1: "human",
    -1: "alphabeta",
}

player_depths = {
    1: 2,
    -1: 2,
}

agents = {
    1: None,
    -1: None,
}

mode = "human_vs_ai"


def detect_mode():
    has_black_human = (player_types[1] == "human")
    has_white_human = (player_types[-1] == "human")

    if has_black_human and has_white_human:
        return "human_vs_human"
    elif has_black_human or has_white_human:
        return "human_vs_ai"
    else:
        return "ai_vs_ai"


def make_agent(player):
    t = player_types[player]
    depth = player_depths[player]

    if t == "human":
        return None
    elif t == "random":
        return RandomAgent(proximity=PROXIMITY)
    elif t == "alphabeta":
        return AlphaBetaAgent(depth=depth, proximity=PROXIMITY)
    elif t == "minimax":
        return MinimaxAgent(depth=depth, proximity=PROXIMITY)
    else:
        return None


def rebuild_agents():
    global agents
    agents = {
        1: make_agent(1),
        -1: make_agent(-1),
    }


def reset_game():
    global board, current_player, last_move, winner, mode
    board = Board()
    current_player = 1
    last_move = None
    winner = None
    rebuild_agents()
    mode = detect_mode()


reset_game()


def serialize_board(b: Board):
    return b.board


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/state", methods=["GET"])
def get_state():
    return jsonify({
        "board": serialize_board(board),
        "n": board.n,
        "currentPlayer": current_player,
        "lastMove": last_move,
        "winner": winner,
        "mode": mode,
        "playerTypes": {
            "black": player_types[1],
            "white": player_types[-1],
        },
        "playerDepths": {
            "black": player_depths[1],
            "white": player_depths[-1],
        },
    })


@app.route("/reset", methods=["POST"])
def reset():
    global player_types, player_depths

    data = request.get_json(silent=True) or {}
    config = data.get("config", {})

    black_cfg = config.get("black")
    white_cfg = config.get("white")

    if black_cfg:
        t = black_cfg.get("type", player_types[1])
        d = black_cfg.get("depth", player_depths[1])
        player_types[1] = t
        try:
            player_depths[1] = int(d)
        except (TypeError, ValueError):
            player_depths[1] = player_depths[1]

    if white_cfg:
        t = white_cfg.get("type", player_types[-1])
        d = white_cfg.get("depth", player_depths[-1])
        player_types[-1] = t
        try:
            player_depths[-1] = int(d)
        except (TypeError, ValueError):
            player_depths[-1] = player_depths[-1]

    reset_game()

    return jsonify({
        "status": "ok",
        "mode": mode,
        "playerTypes": {
            "black": player_types[1],
            "white": player_types[-1],
        },
        "playerDepths": {
            "black": player_depths[1],
            "white": player_depths[-1],
        },
    })


@app.route("/move", methods=["POST"])
def human_move():
    global current_player, last_move, winner

    if winner is not None:
        return jsonify({"error": "Game already finished", "winner": winner}), 400

    if player_types[current_player] != "human":
        return jsonify({"error": "It's not a human player's turn"}), 400

    data = request.get_json()
    r = data.get("row")
    c = data.get("col")

    try:
        board.move(r, c, current_player)
    except Exception as e:
        return jsonify({"error": f"Invalid move: {e}"}), 400

    last_move = (r, c)

    term, win = board.is_terminal_state(last_move=last_move, player=current_player)
    if term:
        winner = win
        current_player = None
        return jsonify(build_state_response(aiMove=None))

    current_player = -current_player

    aiMove = None
    if player_types[current_player] != "human":
        aiMove = perform_ai_move()

    return jsonify(build_state_response(aiMove=aiMove))


def perform_ai_move():
    global current_player, last_move, winner

    if winner is not None:
        return None

    if player_types[current_player] == "human":
        return None

    agent = agents.get(current_player)
    if agent is None:
        return None

    try:
        move = agent.choose_move(board, current_player)
    except TypeError:
        move = agent.choose_move(board)

    if move is None:
        winner = 0
        current_player = None
        return None

    r, c = move
    board.move(r, c, current_player)
    last_move = (r, c)

    term, win = board.is_terminal_state(last_move=last_move, player=current_player)
    if term:
        winner = win
        current_player = None
    else:
        current_player = -current_player

    return {"row": r, "col": c}


@app.route("/step_ai", methods=["POST"])
def step_ai():
    global current_player, winner

    if winner is not None:
        return jsonify(build_state_response())

    if player_types[current_player] == "human":
        return jsonify(build_state_response())

    aiMove = perform_ai_move()
    return jsonify(build_state_response(aiMove=aiMove))


def build_state_response(aiMove=None):
    return {
        "board": serialize_board(board),
        "n": board.n,
        "currentPlayer": current_player,
        "lastMove": last_move,
        "winner": winner,
        "mode": mode,
        "playerTypes": {
            "black": player_types[1],
            "white": player_types[-1],
        },
        "playerDepths": {
            "black": player_depths[1],
            "white": player_depths[-1],
        },
        "aiMove": aiMove,
    }


if __name__ == "__main__":
    app.run(debug=True)
