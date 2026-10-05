def sieve_of_eratosthenes(n):
    is_prime=[1]*(n+1)
    is_prime[0]=is_prime[1]=0
    for i in range(2,int(n**0.5)+1):
        if is_prime[i]:
            for j in range(i*i,n+1,i):
                is_prime[j]=0
    return is_prime
def main():
    ps=sieve_of_eratosthenes(200000)
    I=open(0).readline
    n,a,b=map(int,I().split())
    f=lambda x:([b,a][ps[x]])
    m=[tuple(map(int,I().split()))for _ in range(2)]
    dp=[0]*n
    dp[0]=f(m[0][0]+m[1][0])
    if n==1:return print(dp[0])
    dp[1]=max(f(m[0][0]+m[1][0])+f(m[0][1]+m[1][1]),f(sum(m[0][:2]))+f(sum(m[1][:2])))
    for i in range(2,n):dp[i]=max(dp[i-1]+f(m[0][i]+m[1][i]),dp[i-2]+f(sum(m[0][i-1:i+1]))+f(sum(m[1][i-1:i+1])))
    print(dp[-1])
main()