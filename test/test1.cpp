#include <bits/stdc++.h>
using namespace std;
struct Solver {
 long long R; int N, fullMask; vector<int> deck; array<int,2> P{},D{}; vector<int> ps,ds;
 static int cv(const string&s){char c=s[0]; if(c=='A') return 1; if(c>='2'&&c<='9') return c-'0'; return 10;}
 int score(const array<int,2>& a,int m){int x=a[0]+a[1]; bool ace=a[0]==1||a[1]==1; for(int i=0;i<N;i++) if(m>>i&1){x+=deck[i]; ace|=deck[i]==1;} return ace&&x+10<=21?x+10:x;}
 static int init(const array<int,2>&a){int x=a[0]+a[1]; bool ace=a[0]==1||a[1]==1; return ace&&x+10<=21?x+10:x;}
 double G(int p,int d){int pv=ps[p],dv=ds[d],rem=fullMask&~(p|d); if(dv>21) return 1; if(dv>=17||!rem) return pv>dv?1:pv<dv?-1:0; double z=0; int c=__builtin_popcount((unsigned)rem); for(int b=rem;b;b&=b-1){int bit=b&-b; z+=G(p,d|bit);} return z/c;}
 double F(int p){int pv=ps[p],rem=fullMask&~p; if(pv>21) return -1; double stay=G(p,0); if(pv==21||!rem) return stay; double hit=0; int c=__builtin_popcount((unsigned)rem); for(int b=rem;b;b&=b-1){int bit=b&-b,n=p|bit; hit+=(ps[n]>21?-1:F(n));} return max(stay,hit/c);}
 long double run(){bool pb=init(P)==21,db=init(D)==21; if(pb||db){if(pb&&db)return 0; if(pb)return 1.5L*R; return -(long double)R;} fullMask=(1<<N)-1; ps.resize(1<<N);ds.resize(1<<N);for(int m=0;m<(1<<N);m++){ps[m]=score(P,m);ds[m]=score(D,m);} return (long double)F(0)*R;}
};
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int T;cin>>T;cout<<fixed<<setprecision(12);while(T--){Solver s;cin>>s.R>>s.N;string c;for(int i=0;i<2;i++){cin>>c;s.P[i]=Solver::cv(c);}for(int i=0;i<2;i++){cin>>c;s.D[i]=Solver::cv(c);}s.deck.resize(s.N);for(int i=0;i<s.N;i++){cin>>c;s.deck[i]=Solver::cv(c);}cout<<s.run()<<'\n';}}