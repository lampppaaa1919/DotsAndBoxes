import math
import numpy as np

ALPHA = -np.inf
BETA = np.inf


def minimax(game, state, depth, is_maximizing, alpha=ALPHA, beta=BETA):

    if depth == 0 or game.goal_test(state):
        return game.h(state)

    succs = game.successor(state)

    if is_maximizing:
        maxEval = ALPHA
        for action, new_state in succs.items():
            eval = minimax(game, new_state, depth - 1, False, alpha, beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
        return maxEval
    else:
        minEval = BETA
        for action, new_state in succs.items():
            eval = minimax(game, new_state, depth - 1, True,alpha,beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
        return minEval

def minimax_prune(game, state, depth, is_maximizing, alpha=ALPHA, beta=BETA):

    if depth == 0 or game.goal_test(state):
        return game.h(state)

    succs = game.successor(state)
    if is_maximizing:
        max_eval = ALPHA
        for action, new_state in succs.items():
            eval = minimax(game, new_state, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        minEval = BETA
        for action, new_state in succs.items():
            eval = minimax(game, new_state, depth - 1, True,alpha,beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def minimax_asc(game, state, depth, is_maximizing, alpha=ALPHA, beta=BETA):

    if depth == 0 or game.goal_test(state):
        return game.h(state)

    succs = game.successor(state)

    ordered = sorted(succs.items(),
                     key=lambda i: game.h(i[1]),
                     reverse=False)

    if is_maximizing:
        maxEval = ALPHA
        for action, new_state in ordered:
            eval = minimax_asc(game, new_state, depth - 1, False, alpha,beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        min_eval = BETA
        for action, new_state in ordered:
            eval = minimax_asc(game, new_state, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def minimax_desc(game, state, depth, is_maximizing, alpha=ALPHA, beta=BETA):

    if depth == 0 or game.goal_test(state):
        return game.h(state)

    succs = game.successor(state)

    ordered = sorted(succs.items(), key=lambda i: game.h(i[1]), reverse=is_maximizing)

    if is_maximizing:
        maxEval = ALPHA
        for action, new_state in ordered:
            eval = minimax_desc(game, new_state, depth - 1, False, alpha,beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = BETA
        for action, new_state in ordered:
            eval = minimax_desc(game, new_state, depth - 1, False, alpha, beta)
            min_eval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def best_move(game, state, depth, is_maximizing, case = 2):
    best_val = ALPHA
    best_action = None
    successors = game.successor(state)
    for action, new_state in successors.items():

        eval = BETA

        if case ==1: eval = minimax(game, new_state, depth - 1, not is_maximizing)
        elif case==2: eval = minimax_prune(game, new_state, depth - 1, not is_maximizing)
        elif case==3: eval = minimax_asc(game, new_state, depth - 1, not is_maximizing)
        elif case==4: eval = minimax_desc(game, new_state, depth - 1, not is_maximizing)

        if eval > best_val:
            best_val = eval
            best_action = action
    return best_action
