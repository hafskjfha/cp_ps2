"""Append sparse permutation powers while preserving every existing operation."""


def route_extra_powers(n,d,board,target,stamp,k,powers):
    indices,_,_,_,_=build(n,d,target)
    side=n-d+1
    answer=[]
    for power in powers:
        left=k-len(answer)
        if left<2*power:continue
        tail=route_tail(n,d,board,target,stamp,left,(power,),1)
        for x,y,r in tail:
            transition(board,stamp,indices[(x*side+y)*4+r])
        answer.extend(tail)
    return answer
