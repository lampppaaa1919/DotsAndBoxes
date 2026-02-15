"""se presmetuvaat site mozni potezi vo partija igra"""
def minimax(state,depth,turn):
    if depth == 0 or state.isGoal:
        return state
    if turn == "agent-a":
        maxEval = -int("inf")
        for succ in state.succs:
            eval = minimax(succ,depth-1,"agent-b")
            maxEval = max(maxEval,eval)
        return maxEval
    else:
        minEval = int("inf")
        for succ in state.succs:
            eval = minimax(succ,depth-1,"agent-a")
            minEval = min(minEval,eval)
        return minEval

"""se presmetuvaat site najdobri potezi vo partija igra"""
def minimax_ab(state,depth,alpha,beta,turn):
    if depth == 0 or state.isGoal:
        return state
    if turn == "agent-a":
        maxEval = -int("inf")
        for succ in state.succs:
            eval = minimax_ab(succ,depth-1,alpha,beta,"agent-b")
            alpha = max(alpha,eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = int("inf")
        for succ in state.succs:
            eval = minimax_ab(succ,depth-1,alpha,beta,"agent-a")
            beta = min(beta,eval)
            if beta <= alpha:
                break
        return minEval

"""se presmetuvaat najdobrite potezi podredeni po volja na agent A - igrach"""
def minimax_ab_sorted(state,depth,alpha,beta,turn):
    if depth == 0 or state.isGoal:
        return state
    if turn == "agent-a":
        maxEval = -int("inf")
        sorted_succs=sorted(state.succs,key=(lambda succ: succ.value))
        for succ in sorted_succs:
            eval = minimax_ab(succ,depth-1,alpha,beta,"agent-b")
            alpha = max(alpha,eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = int("inf")
        sorted_succs = sorted(state.succs, key=(lambda succ: succ.value))
        for succ in sorted_succs:
            eval = minimax_ab_sorted(succ,depth-1,alpha,beta,"agent-a")
            beta = min(beta,eval)
            if beta <= alpha:
                break
        return minEval

"""se presmetuvaat najdobrite potezi podredeni po volja na agent B - protivnik"""
def minimax_ab_sorted_r(state,depth,alpha,beta,turn):
    if depth == 0 or state.isGoal:
        return state
    if turn == "agent-a":
        maxEval = -int("inf")
        sorted_succs=sorted(state.succs,key=(lambda succ: succ.value),reverse=True)
        for succ in sorted_succs:
            eval = minimax_ab(succ,depth-1,alpha,beta,"agent-b")
            alpha = max(alpha,eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = int("inf")
        sorted_succs = sorted(state.succs, key=(lambda succ: succ.value), reverse=True)
        for succ in sorted_succs:
            eval = minimax_ab_sorted(succ,depth-1,alpha,beta,"agent-a")
            beta = min(beta,eval)
            if beta <= alpha:
                break
        return minEval