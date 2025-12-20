from Board import Board
from HeuristicMinimaxAgent import MinimaxAgent
from AlphaBetaAgent import AlphaBetaAgent
from RandomAgent import RandomAgent
import csv


def get_agent_args(agent):
    if hasattr(agent, "max_depth"):
        return (agent.max_depth, agent.proximity)
    else:
        return (agent.proximity,)


def describe_agent(agent):
    cls_name = type(agent).__name__
    if isinstance(agent, AlphaBetaAgent):
        if agent.max_depth == 1:
            return "MinimaxAgent_Depth1"
        return f"{cls_name}_Depth{agent.max_depth}"
    if isinstance(agent, MinimaxAgent):
        return f"{cls_name}_Depth{agent.max_depth}"
    return cls_name


def compute_phase_averages(move_times, total_moves):
    if total_moves == 0 or not move_times:
        return 0.0, 0.0, 0.0, 0.0

    t1 = total_moves // 3
    t2 = (2 * total_moves) // 3

    early = []
    mid = []
    late = []
    all_t = []

    for idx, t in move_times:
        all_t.append(t)
        if idx <= t1:
            early.append(t)
        elif idx <= t2:
            mid.append(t)
        else:
            late.append(t)

    def avg(lst):
        return sum(lst) / len(lst) if lst else 0.0

    return avg(early), avg(mid), avg(late), avg(all_t)


def play_match(agent1, agent2, board_size=15):
    board = Board(board_size)
    player = 1
    agents = {1: agent1, -1: agent2}

    stats = {
        "nodes_1": 0, "nodes_2": 0,
        "time_1": 0.0, "time_2": 0.0,
        "cutoffs_1": 0, "cutoffs_2": 0,
        "moves": 0,
        "move_times_1": [],
        "move_times_2": []
    }

    while True:
        ag = agents[player]
        move = ag.choose_move(board, player)

        if move is None:
            return 0, stats

        r, c = move
        board.move(r, c, player)

        stats["moves"] += 1
        mindex = stats["moves"]

        if player == 1:
            stats["nodes_1"] += ag.nodes_expanded
            stats["time_1"] += ag.last_move_time
            stats["move_times_1"].append((mindex, ag.last_move_time))
            if hasattr(ag, "cutoffs"):
                stats["cutoffs_1"] += ag.cutoffs
        else:
            stats["nodes_2"] += ag.nodes_expanded
            stats["time_2"] += ag.last_move_time
            stats["move_times_2"].append((mindex, ag.last_move_time))
            if hasattr(ag, "cutoffs"):
                stats["cutoffs_2"] += ag.cutoffs

        term, winner = board.is_terminal_state((r, c), player)
        if term:
            return winner, stats

        player *= -1


def run_matchup(name, agentA_proto, agentB_proto, games, board_size=15):
    print(f"\n=== MATCHUP: {name} ({games} games) ===")

    records = []

    agent1_label = describe_agent(agentA_proto)
    agent2_label = describe_agent(agentB_proto)

    wins1 = 0
    wins2 = 0

    half = games // 2

    for g in range(games):
        A = type(agentA_proto)(*get_agent_args(agentA_proto))
        B = type(agentB_proto)(*get_agent_args(agentB_proto))

        if g < half:
            starter = agent1_label
            winner_sign, stats = play_match(A, B, board_size)

            nodes1, nodes2 = stats["nodes_1"], stats["nodes_2"]
            time1, time2 = stats["time_1"], stats["time_2"]
            cuts1, cuts2 = stats["cutoffs_1"], stats["cutoffs_2"]
            mt1, mt2 = stats["move_times_1"], stats["move_times_2"]

            if winner_sign == 1:
                winner = agent1_label
                wins1 += 1
            elif winner_sign == -1:
                winner = agent2_label
                wins2 += 1
            else:
                winner = "Draw"

        else:
            starter = agent2_label
            winner_sign, stats = play_match(B, A, board_size)

            nodes2, nodes1 = stats["nodes_1"], stats["nodes_2"]
            time2, time1 = stats["time_1"], stats["time_2"]
            cuts2, cuts1 = stats["cutoffs_1"], stats["cutoffs_2"]
            mt2, mt1 = stats["move_times_1"], stats["move_times_2"]

            if winner_sign == 1:
                winner = agent2_label
                wins2 += 1
            elif winner_sign == -1:
                winner = agent1_label
                wins1 += 1
            else:
                winner = "Draw"

        total_moves = stats["moves"]

        e1, m1, l1, o1 = compute_phase_averages(mt1, total_moves)
        e2, m2, l2, o2 = compute_phase_averages(mt2, total_moves)

        rec = {
            "matchup": name,
            "game": g + 1,
            "starter": starter,
            "winner": winner,
            "agent1": agent1_label,
            "agent2": agent2_label,
            "nodes_agent1": nodes1,
            "nodes_agent2": nodes2,
            "time_agent1": time1,
            "time_agent2": time2,
            "cutoffs_agent1": cuts1,
            "cutoffs_agent2": cuts2,
            "moves": total_moves,
            "avg_time_early_agent1": e1,
            "avg_time_mid_agent1": m1,
            "avg_time_late_agent1": l1,
            "avg_time_overall_agent1": o1,
            "avg_time_early_agent2": e2,
            "avg_time_mid_agent2": m2,
            "avg_time_late_agent2": l2,
            "avg_time_overall_agent2": o2,
            "win_rate_agent1": None,
            "win_rate_agent2": None,
        }
        records.append(rec)
        print(f"  -> Game {g+1}/{games} finished")

    wr1 = wins1 / games
    wr2 = wins2 / games

    for rec in records:
        rec["win_rate_agent1"] = wr1
        rec["win_rate_agent2"] = wr2

    return records


def export_csv(filename, records):
    keys = [
        "matchup", "game", "starter", "winner", "agent1", "agent2",
        "nodes_agent1", "nodes_agent2",
        "time_agent1", "time_agent2",
        "cutoffs_agent1", "cutoffs_agent2",
        "moves",
        "avg_time_early_agent1", "avg_time_mid_agent1",
        "avg_time_late_agent1", "avg_time_overall_agent1",
        "avg_time_early_agent2", "avg_time_mid_agent2",
        "avg_time_late_agent2", "avg_time_overall_agent2",
        "win_rate_agent1", "win_rate_agent2",
    ]
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)
    print(f"\nCSV saved to {filename}\n")


def run_all_experiments():
    all_records = []

    all_records += run_matchup(
        "AB_d2_vs_Random",
        AlphaBetaAgent(depth=2, proximity=2),
        RandomAgent(proximity=2),
        games=6,
        board_size=15
    )

    all_records += run_matchup(
        "Minimax_d1_vs_Random",
        AlphaBetaAgent(depth=1, proximity=2),
        RandomAgent(proximity=2),
        games=6,
        board_size=15
    )

    all_records += run_matchup(
        "AB_d2_vs_Minimax_d1",
        AlphaBetaAgent(depth=2, proximity=2),
        AlphaBetaAgent(depth=1, proximity=2),
        games=30,
        board_size=15
    )

    export_csv("gomoku_random_tests_&_AB_d2_vs_Minimax_d1.csv", all_records)


if __name__ == "__main__":
    run_all_experiments()
