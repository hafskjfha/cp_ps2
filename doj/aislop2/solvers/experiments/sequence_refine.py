"""Greedy construction followed by exact backward sequence coordinate descent."""
import sys


def build_actions(n, d):
    rotations = []
    for r in range(4):
        offsets = []
        for u in range(d):
            for v in range(d):
                p,q = ((u,v),(v,d-1-u),(d-1-u,d-1-v),(d-1-v,u))[r]
                offsets.append(p*n+q)
        rotations.append(offsets)
    return [(tuple(x*n+y+v for v in rotations[r]),(x,y,r))
            for x in range(n-d+1) for y in range(n-d+1) for r in range(4)]


def transition(state, nn, indices):
    for j,pos in enumerate(indices):
        state[nn+j],state[pos] = state[pos],state[nn+j]


def best_action(state, wishes, actions, nn, dd, current=-1):
    grid,wanted = state[:nn],wishes[:nn]
    losses = [value == goal for value,goal in zip(grid,wanted)]
    rows = []
    for j in range(dd):
        carried,goal = state[nn+j],wishes[nn+j]
        fixed_loss = carried == goal
        rows.append([(carried == desire)+(value == goal)-loss-fixed_loss
                     for value,desire,loss in zip(grid,wanted,losses)])
    best_id,best_gain = -1,0
    if current >= 0:
        old = sum(rows[j][pos] for j,pos in enumerate(actions[current][0]))
        if old >= 0:
            best_id,best_gain = current,old
    if dd == 4:
        g0,g1,g2,g3 = rows
        for aid,(p,_) in enumerate(actions):
            gain = g0[p[0]]+g1[p[1]]+g2[p[2]]+g3[p[3]]
            if gain > best_gain:
                best_id,best_gain = aid,gain
    else:
        g0,g1,g2,g3,g4,g5,g6,g7,g8 = rows
        for aid,(p,_) in enumerate(actions):
            gain = (g0[p[0]]+g1[p[1]]+g2[p[2]]+g3[p[3]]+g4[p[4]]+
                    g5[p[5]]+g6[p[6]]+g7[p[7]]+g8[p[8]])
            if gain > best_gain:
                best_id,best_gain = aid,gain
    return best_id,best_gain


def greedy(n,d,k,grid,target,stamp,actions):
    nn,dd = n*n,d*d
    state,wishes = grid+stamp,target+[-1]*dd
    sequence = []
    for _ in range(k):
        aid,gain = best_action(state,wishes,actions,nn,dd)
        if gain <= 0:
            break
        transition(state,nn,actions[aid][0])
        sequence.append(aid)
    return sequence


def refine(n,d,k,initial,target,actions,sequence,passes=3):
    nn,dd = n*n,d*d
    for _ in range(passes):
        sequence = sequence+[-1]*min(4,k-len(sequence))
        states = [initial[:]]
        for aid in sequence:
            state = states[-1][:]
            if aid >= 0:
                transition(state,nn,actions[aid][0])
            states.append(state)
        wishes = target+[-1]*dd
        changed = False
        for i in range(len(sequence)-1,-1,-1):
            old = sequence[i]
            chosen,_ = best_action(states[i],wishes,actions,nn,dd,old)
            if chosen != old:
                sequence[i] = chosen
                changed = True
            if chosen >= 0:
                transition(wishes,nn,actions[chosen][0])
        sequence = [aid for aid in sequence if aid >= 0]
        if not changed:
            break
    return sequence


def solve(n,d,c,k,grid,target,stamp):
    actions = build_actions(n,d)
    sequence = greedy(n,d,k,grid,target,stamp,actions)
    sequence = refine(n,d,k,grid+stamp,target,actions,sequence)
    return [actions[aid][1] for aid in sequence]


def main():
    data = list(map(int,sys.stdin.buffer.read().split()))
    n,d,c,k = data[:4]
    nn = n*n
    operations = solve(n,d,c,k,data[4:4+nn],data[4+nn:4+2*nn],data[4+2*nn:])
    print(len(operations))
    for operation in operations:
        print(*operation)


if __name__ == '__main__':
    main()
