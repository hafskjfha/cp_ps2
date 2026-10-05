from collections import deque
input=open(0).readline
for _ in range(int(input())):
    m,t=map(int,input().split())
    delta=[*map(int,input().split())]
    q=deque([(0,0)])
    ans_a=ans_b=float('inf')
    v=set([0])
    while q:
        x,y=q.popleft()
        if x==t:
            ans_a,ans_b=y,0
            break
        for dx in delta:
            nx=min(max(0,x+dx),3600)
            if 0<=nx<3601 and nx not in v:
                v.add(nx)
                q.append((nx,y+1))
                #print(nx,y+1)
                if nx>=t and ans_a>=y+1:
                    ans_a=min(ans_a,y+1)
                    ans_b=min(ans_b,nx-t)
    #print(f"TC #{_+1}")
    print(ans_a,ans_b)
   # print("==========")