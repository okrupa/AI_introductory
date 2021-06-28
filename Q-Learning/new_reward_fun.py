def to_s(row, col, ncol):
    return row * ncol + col


def inc(row, col, a, nrow, ncol):
    if a == 0:
        col = max(col - 1, 0)
    elif a == 1:
        row = min(row + 1, nrow - 1)
    elif a == 2:
        col = min(col + 1, ncol - 1)
    elif a == 3:
        row = max(row - 1, 0)
    return (row, col)


def update_nex_state(row, col, action, env, nrow, ncol):
    newrow, newcol = inc(row, col, action, nrow, ncol)
    newstate = to_s(newrow, newcol, ncol)
    newletter = env.desc[newrow, newcol]
    done = bytes(newletter) in b'GH'
    reward = 0
    if newletter == b'G':
        reward = 1.0
    elif newletter == b'H':
        reward = -1.0
    elif (row == 0 and action == 3) or (row == 7 and action == 1) or (col == 0 and action == 0) or (col == 7 and action == 2):
        reward = -0.1
    return newstate, reward, done



def create_reward_function(nA, nS, env, is_slippery=True):

    nrow = env.nrow
    ncol = env.ncol

    newP = {s: {a: [] for a in range(nA)} for s in range(nS)}

    for row in range(nrow):
        for col in range(ncol):
            s = to_s(row, col, ncol)
            for a in range(4):
                li = newP[s][a]
                letter = env.desc[row, col]
                if letter in b'GH':
                    li.append((1.0, s, 0, True))
                else:
                    if is_slippery:
                        for b in [(a - 1) % 4, a, (a + 1) % 4]:
                            li.append((
                                1. / 3.,
                                *update_nex_state(row, col, b, env, nrow, ncol)
                            ))
                    else:
                        li.append((
                            1., *update_nex_state(row, col, a, env, nrow, ncol)
                        ))
    env.P = newP


