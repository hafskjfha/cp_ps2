from collections import deque
import sys

input = sys.stdin.readline

n,t = map(int,input().split())

arr = sorted(list(map(int,input().split())))

answer = n

l, r = 1,n

while l <= r:
    mid = (l+r) // 2
    queue = deque([])
    fail = False
    for i in range(n):
        left = max(1,arr[i]-(t-1))
        while queue:
            if queue[0] + (t-1) < arr[i] - (t-1): queue.popleft()
            else: break
        if len(queue) < mid:
            queue.append(left)
            continue
        if queue[0] + (t-1) >= arr[i]:
            fail = True
            break
        else:
            queue.append(max(queue[0]+t,arr[i]-(t-1)))
        queue.popleft()
    if fail:
        l = mid + 1
    else:
        answer = mid
        r = mid - 1

print(answer)