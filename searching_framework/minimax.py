"""se presmetuvaat site mozni potezi vo partija igra"""
import math


def minimax(game, state, depth, is_maximizing):
    if depth == 0 or game.goal_test(state):
        return game.h(state)
    succs = game.successor(state)
    if is_maximizing:
        maxEval = -int("inf")
        for action, new_state in succs.items():
            eval = minimax(game, new_state, depth - 1, False)
            maxEval = max(maxEval, eval)
        return maxEval
    else:
        minEval = int("inf")
        for action, new_state in succs.items():
            eval = minimax(game, new_state, depth - 1, True)
            minEval = min(minEval, eval)
        return minEval

def best_move(game, state, depth):
    best_val = -math.inf
    best_action = None
    successors = game.successor(state)
    for action, new_state in successors.items():
        eval = minimax(game, new_state, depth - 1, False)
        if eval > best_val:
            best_val = eval
            best_action = action
        return best_action

"""se presmetuvaat site najdobri potezi vo partija igra"""


def minimax_ab(state, depth, alpha, beta, turn):
    if depth == 0 or state.isGoal:
        return state
    if turn == "agent-a":
        maxEval = -int("inf")
        for succ in state.succs:
            eval = minimax_ab(succ, depth - 1, alpha, beta, "agent-b")
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = int("inf")
        for succ in state.succs:
            eval = minimax_ab(succ, depth - 1, alpha, beta, "agent-a")
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval


"""se presmetuvaat najdobrite potezi podredeni po volja na agent A - igrach"""


def minimax_ab_sorted(state, depth, alpha, beta, turn):
    if depth == 0 or state.isGoal:
        return state
    if turn == "agent-a":
        maxEval = -int("inf")
        sorted_succs = sorted(state.succs, key=(lambda succ: succ.value))
        for succ in sorted_succs:
            eval = minimax_ab(succ, depth - 1, alpha, beta, "agent-b")
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = int("inf")
        sorted_succs = sorted(state.succs, key=(lambda succ: succ.value))
        for succ in sorted_succs:
            eval = minimax_ab_sorted(succ, depth - 1, alpha, beta, "agent-a")
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval


"""se presmetuvaat najdobrite potezi podredeni po volja na agent B - protivnik"""


def minimax_ab_sorted_r(state, depth, alpha, beta, turn):
    if depth == 0 or state.isGoal:
        return state
    if turn == "agent-a":
        maxEval = -int("inf")
        sorted_succs = sorted(state.succs, key=(lambda succ: succ.value), reverse=True)
        for succ in sorted_succs:
            eval = minimax_ab(succ, depth - 1, alpha, beta, "agent-b")
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = int("inf")
        sorted_succs = sorted(state.succs, key=(lambda succ: succ.value), reverse=True)
        for succ in sorted_succs:
            eval = minimax_ab_sorted(succ, depth - 1, alpha, beta, "agent-a")
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
