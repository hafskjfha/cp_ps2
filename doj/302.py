import sys

def main():
    input=sys.stdin.readline
    h1,m1=map(int,input().split(':'))
    h2,m2=map(int,input().split(':'))
    h1-=1
    h2-=1
    
    print(min(abs(h1*60+m1-(h2*60+m2)),abs((h1+12)*60+m1-(h2*60+m2)),abs((h1)*60+m1-((h2+12)*60+m2)))*6)
    
    
main()