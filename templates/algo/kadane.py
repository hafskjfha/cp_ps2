# 부분합 최대/최소
def kadane(a):
    cur = best = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

def kadane_with_range(a):
    cur = best = a[0]
    cur_l = best_l = best_r = 0

    for i in range(1, len(a)):
        if a[i] > cur + a[i]:
            cur = a[i]
            cur_l = i
        else:
            cur += a[i]

        if cur > best:
            best = cur
            best_l, best_r = cur_l, i

    return best, best_l, best_r