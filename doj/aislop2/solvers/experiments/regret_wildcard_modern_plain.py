import random
import sys
_a=12
_b=True
def _c(a,b):
 c,d=([0]*6,[0]*6)
 for e in a:
  c[e]+=1
 for e in b:
  d[e]+=1
 return sum((min(f,g)for f,g in zip(c,d)))
def _d(a,b,c):
 d=[]
 for e in range(4):
  d.append([s*a+t for q in range(b)for r in range(b)for s,t in[((q,r),(r,b-1-q),(b-1-q,b-1-r),(b-1-r,q))[e]]])
 f,g,h=([],[],[])
 i=[[]for _ in range(a*a)]
 j=[]
 for k in range(a-b+1):
  for l in range(a-b+1):
   m=len(j)
   n=[k*a+l+q for q in d[0]]
   j.append(n)
   for o in n:
    i[o].append(m)
   for e in range(4):
    p=tuple((k*a+l+q for q in d[e]))
    f.append(p)
    g.append(sum((1<<6*q+c[r]for q,r in enumerate(p))))
    h.append((k,l,e))
 return(f,g,h,i,j)
def _e(a,b,c):
 for d,e in enumerate(c):
  b[d],a[e]=(a[e],b[d])
def _f(a,b,c,d,e,f,g):
 h=sum((A==B for A,B in zip(e,f)))
 i=_c(e+g,f)
 if h==i:
  return[]
 j,k=(h,[])
 l=917351
 for m in e+f+g:
  l=(l^m)*1000003&4294967295
 n=random.Random(l)
 o=list(range(4*(a-b+1)**2))
 for p in range(_a):
  if p:
   n.shuffle(o)
  q=_g(a,b,c,e[:],f,g[:],o[:])
  r,s=(h,[])
  t=set()
  for u in range(d):
   t.add(tuple(q.J))
   v,w=q.g()
   if v<0 or(v==0 and(not _b or p==0)):
    break
   x=-1
   while w:
    y=w&-w
    z=q.z[y.bit_length()-1]
    if v>0 or tuple((q.q[A]for A in q.b[z][0]))not in t:
     x=z
     break
    w^=y
   if x<0:
    break
   if v>0:
    t.clear()
   q.e(x)
   r+=v
   s.append(q.b[x][1])
   if r>j:
    j,k=(r,s[:])
   if j==i:
    return k
 return k
class _g:
 _geometry_cache=None
 def __init__(a,b,c,d,e,f,g,h=None):
  a.w,a.k,a.h=(b,c,d)
  a.q,a.M,a.J=(e,f,g)
  a.u=sum((C==D for C,D in zip(e,f)))
  a.s=_c(e+g,f)
  key=(b,c,d,tuple(f))
  i=_g._geometry_cache
  if i is not None and i[0]==key:
   a.F,a.b,a.t,a.j=i[1:]
  else:
   a.F=[]
   a.b=[]
   a.t=[]
   a.j=[[]for _ in e]
   j=[]
   for k in range(4):
    l=[]
    for m in range(c):
     for n in range(c):
      o,p=((m,n),(n,c-1-m),(c-1-m,c-1-n),(c-1-n,m))[k]
      l.append(o*b+p)
    j.append(l)
   for q in range(b-c+1):
    for r in range(b-c+1):
     s=q*b+r
     t=tuple((s+C for C in j[0]))
     u=len(a.F)
     a.F.append(t)
     for o in t:
      a.j[o].append(u)
     for k in range(4):
      t=tuple((s+C for C in j[k]))
      a.b.append((t,(q,r,k)))
      a.t.append(sum((1<<d*C+f[D]for C,D in enumerate(t))))
   _g._geometry_cache=(key,a.F,a.b,a.t,a.j)
  a.z=list(range(len(a.b)))if h is None else h
  a.i=[sum((e[D]==f[D]for D in C))for C in a.F]
  a.K=sum((1<<d*C+D for C,D in enumerate(g)))
  a.I=c*c
  a.c=(1<<len(a.b))-1
  a.N=[[0]*d for _ in g]
  a.E=[0]*len(a.F)
  for v,w in enumerate(a.z):
   x=1<<v
   a.E[w>>2]|=x
   for y,o in enumerate(a.b[w][0]):
    a.N[y][f[o]]|=x
  a.y=[0]*4
  for u,z in enumerate(a.i):
   A=a.I-z
   for B in range(4):
    if A&1<<B:
     a.y[B]|=a.E[u]
 def o(a,b):
  return(a.K&a.t[b]).bit_count()-a.i[b>>2]
 def e(a,b):
  c,_=a.b[b]
  d,e,f=(a.q,a.J,a.M)
  g={}
  for h,i in enumerate(c):
   j,k=(d[i],e[h])
   e[h],d[i]=(j,k)
   l=(k==f[i])-(j==f[i])
   a.u+=l
   if l:
    for m in a.j[i]:
     g[m]=g.get(m,0)+l
  n,o,p=(a.i,a.y,a.E)
  q=a.I
  for m,l in g.items():
   if not l:
    continue
   j=n[m]
   k=j+l
   n[m]=k
   r=q-j^q-k
   s=p[m]
   while r:
    t=r&-r
    o[t.bit_length()-1]^=s
    r^=t
  u=a.h
  a.K=sum((1<<u*v+w for v,w in enumerate(e)))
 def g(a):
  b=[0]*5
  for c,d in enumerate(a.J):
   e=a.N[c][d]
   f=0
   while e:
    g=b[f]
    b[f]=g^e
    e&=g
    f+=1
  e=0
  for f in range(4):
   h,i=(b[f],a.y[f])
   j=h^i
   b[f]=j^e
   e=h&i|j&e
  b[4]=e
  k,l=(a.c,0)
  for f in range(4,-1,-1):
   m=k&b[f]
   if m:
    k=m
    l|=1<<f
  return(l-a.I,k)
 def f(a):
  b,c=a.g()
  d=(c&-c).bit_length()-1
  return(b,a.z[d])
 def n(a,b,width=64,min_gain=-2):
  c,d=(a.K,a.i)
  e=[(c&w).bit_count()-d[v>>2]for v,w in enumerate(a.t)]
  f=[v for v,w in enumerate(e)if w>=min_gain]
  b.shuffle(f)
  g=sorted(f,key=lambda v:e[v],reverse=True)[:8]
  h=g+f
  i,j=(set(),set())
  k,l=(0,None)
  m=0
  for n in h:
   if n in j:
    continue
   j.add(n)
   o,_=a.b[n]
   p=tuple((a.q[v]for v in o))
   q=(p,e[n])
   if q in i:
    continue
   i.add(q)
   r=e[n]
   a.e(n)
   s,t=a.f()
   u=r+s
   a.e(n)
   if u>k:
    k,l=(u,(n,t))
   m+=1
   if m>=width:
    break
  return l
def _h(a,b,c,d,e,f,g):
 h=a*101+b*19+c*7+d
 for i in range(0,len(e),11):
  h=h*131+e[i]*7+f[i]&4294967295
 j,k=(-1,[])
 for l in range(8):
  m=random.Random(h+l*87917)
  n=list(range(4*(a-b+1)**2))
  if l:
   m.shuffle(n)
  o=_g(a,b,c,e.copy(),f,g.copy(),n)
  p=[]
  while len(p)<d and o.u<o.s:
   q,r=o.f()
   if q>0:
    o.e(r)
    p.append(o.b[r][1])
   elif len(p)+2<=d:
    s=o.n(m)
    if s is None:
     break
    for r in s:
     o.e(r)
     p.append(o.b[r][1])
   else:
    break
  t=sum((u==v for u,v in zip(o.q,f)))
  if t>j:
   j,k=(t,p)
  if j==o.s:
   break
 return k
def _i(a,b,c,d,e,f,g):
 h=_c(e+g,f)
 if sum((y==z for y,z in zip(e,f)))==h:
  return[]
 i,j,k,l,m=_d(a,b,f)
 width=a-b+1
 n=-1
 o=[]
 for p in(_f,_h,_j):
  q=p(a,b,c,d,e[:],f,g[:])
  r,s=(e[:],g[:])
  for t,u,v in q:
   w=(t*width+u)*4+v
   _e(r,s,i[w])
  x=sum((y==z for y,z in zip(r,f)))
  if x>n:
   n,o=(x,q)
  if x==h:
   break
 return o
import random
import sys
def _j(a,b,c,d,e,f,g):
 h=_g(a,b,c,e,f,g)
 i=a*101+b*19+c*7+d
 for j in range(0,len(e),11):
  i=i*131+e[j]*7+f[j]&4294967295
 k=random.Random(i)
 l=[]
 while len(l)<d and h.u<h.s:
  m,n=h.f()
  if m>0:
   if len(l)+2<=d:
    o=h.n(k,width=8,min_gain=max(1,m-1))
    if o is not None:
     n=o[0]
   h.e(n)
   l.append(h.b[n][1])
  elif len(l)+2<=d:
   o=h.n(k)
   if o is None:
    break
   for n in o:
    h.e(n)
    l.append(h.b[n][1])
  else:
   break
 return l
def _k(a,b,c):
 for d,e in enumerate(c):
  a[b+d],a[e]=(a[e],a[b+d])
def _l(a,wishes,b,c,d,current=-1,allow_zero=False):
 e,f=(a[:c],wishes[:c])
 g=[B==C for B,C in zip(e,f)]
 h=[]
 for i in range(d):
  j,k=(a[c+i],wishes[c+i])
  l=j==k
  h.append([(j==C)+(B==k)-D-l for B,C,D in zip(e,f,g)])
 m,n=(-1,0)
 if current>=0:
  o=sum((h[B][C]for B,C in enumerate(b[current][0])))
  if o>=0:
   m,n=(current,o)
 if d==4:
  p,q,r,s=h
  for t,(u,_)in enumerate(b):
   v=p[u[0]]+q[u[1]]+r[u[2]]+s[u[3]]
   if v>n or(allow_zero and m<0 and(v==n)):
    m,n=(t,v)
 else:
  p,q,r,s,w,x,y,z,A=h
  for t,(u,_)in enumerate(b):
   v=p[u[0]]+q[u[1]]+r[u[2]]+s[u[3]]+w[u[4]]+x[u[5]]+y[u[6]]+z[u[7]]+A[u[8]]
   if v>n or(allow_zero and m<0 and(v==n)):
    m,n=(t,v)
 return(m,n)
_m={}
class _n:
 def __init__(a,b,c,d,e,f,g):
  h,i=(b*b,c*c)
  a.x,a.l=(h,i)
  a.q,a.J=(d[:h],d[h:])
  a.Q,a.R=(e[:],[6]*i)
  a.b,a.z=(f,g)
  j=len(f)
  a.d=(1<<j)-1
  key=(b,c)
  k=_m.get(key)
  if k is None:
   l=[[0]*h for _ in range(i)]
   m=[15<<4*D for D in range(j//4)]
   n=[f[D][0]for D in range(0,j,4)]
   o=[[]for _ in range(h)]
   for p,q in enumerate(n):
    for r in q:
     o[r].append(p)
   for s,(q,_)in enumerate(f):
    t=1<<s
    for u,r in enumerate(q):
     l[u][r]|=t
   k=(l,m,n,o)
   _m[key]=k
  a.B,a.E,a.F,a.j=k
  a.values=[[0]*7 for _ in range(i)]
  a.p=[[0]*7 for _ in range(i)]
  for u in range(i):
   v,w=(a.values[u],a.p[u])
   for r,x in enumerate(a.B[u]):
    v[a.q[r]]|=x
    w[a.Q[r]]|=x
  a.O=[0]*j.bit_length()
  for y,s in enumerate(g):
   t=1<<s
   while y:
    z=y&-y
    a.O[z.bit_length()-1]|=t
    y^=z
  a.i=[sum((a.q[E]==a.Q[E]for E in D))for D in a.F]
  a.y=[0]*5
  for p,A in enumerate(a.i):
   B=i-A
   for C in range(4):
    if B&1<<C:
     a.y[C]|=a.E[p]
 def e(a,b,wishes=False):
  if wishes:
   c,d,e,f=(a.Q,a.R,a.p,a.q)
  else:
   c,d,e,f=(a.q,a.J,a.values,a.Q)
  g=a.i[:]
  h=set()
  i,j,k=(a.B,a.j,a.i)
  for l,m in enumerate(a.b[b][0]):
   n,o=(c[m],d[l])
   if n!=o:
    for p in range(a.l):
     q=i[p][m]
     e[p][n]^=q
     e[p][o]^=q
    r=(o==f[m])-(n==f[m])
    if r:
     h.update(j[m])
     for s in j[m]:
      k[s]+=r
    d[l],c[m]=(n,o)
  for s in h:
   t=a.l-g[s]^a.l-k[s]
   while t:
    u=t&-t
    a.y[u.bit_length()-1]^=a.E[s]
    t^=u
 def f(a):
  b=[0]*5
  for c in range(a.l):
   for d in(a.values[c][a.R[c]],a.p[c][a.J[c]]):
    e=0
    while d:
     f=b[e]
     b[e]=f^d
     d&=f
     e+=1
  d=0
  for e in range(5):
   g,h=(b[e],a.y[e])
   i=g^h
   b[e]=i^d
   d=g&h|i&d
  j,k=(a.d,0)
  for e in range(4,-1,-1):
   l=j&b[e]
   if l:
    j=l
    k|=1<<e
  m=k-a.l-sum((p==q for p,q in zip(a.J,a.R)))
  if m<0:
   return(-1,0)
  for n in reversed(a.O):
   if not j&j-1:
    break
   o=j&~n
   if o:
    j=o
  return((j&-j).bit_length()-1,m)
def _o(a,b,c,d,e,f,g,passes=8,offset=0,seed_offset=0):
 h,i=(a*a,b*b)
 j=_c(d,e)
 k=sum(((u+1)*v for u,v in enumerate(d)))+c*131+seed_offset
 l=random.Random(k)
 for _ in range(offset):
  l.shuffle(list(range(len(f))))
 for m in range(passes):
  g=g+[-1]*min(8,c-len(g))
  n=d[:]
  for o in g:
   if o>=0:
    _k(n,h,f[o][0])
  if sum((u==v for u,v in zip(n,e)))==j:
   return[u for u in g if u>=0]
  p=list(range(len(f)))
  l.shuffle(p)
  q=_n(a,b,n,e,f,p)
  for r in range(len(g)-1,-1,-1):
   s=g[r]
   if s>=0:
    q.e(s)
   t,_=q.f()
   g[r]=t
   if t>=0:
    q.e(t,wishes=True)
  g=[u for u in g if u>=0]
 return g
class _p:
 def __init__(a,b,c,d,e,f):
  a.x=f
  a.b=d
  a.H=e[:]
  a.C=[b[:]]
  for g in e:
   h=a.C[-1][:]
   if g>=0:
    _k(h,f,d[g][0])
   a.C.append(h)
  a.Q=[None]*(len(e)+1)
  a.Q[-1]=c+[-1]*(len(b)-f)
  for i in range(len(e)-1,-1,-1):
   j=a.Q[i+1][:]
   if e[i]>=0:
    _k(j,f,d[e[i]][0])
   a.Q[i]=j
  a.G=sum((k==l for k,l in zip(a.C[-1],c)))
 def m(a,b,c):
  d,e=(a.x,a.b)
  f=a.C[b][:]
  g=set(range(d,len(f)))
  for h,i in zip(a.H[b:b+len(c)],c):
   if h>=0:
    g.update(e[h][0])
   if i>=0:
    j=e[i][0]
    g.update(j)
    _k(f,d,j)
  k=a.C[b+len(c)]
  wishes=a.Q[b+len(c)]
  return sum(((f[l]==wishes[l])-(k[l]==wishes[l])for l in g))
 def a(a,b,c,d):
  e,f=(a.x,a.b)
  a.H[b:b+len(c)]=c
  for g in range(b,len(a.H)):
   h=a.C[g][:]
   i=a.H[g]
   if i>=0:
    _k(h,e,f[i][0])
   a.C[g+1]=h
  for g in range(b+len(c)-1,-1,-1):
   j=a.Q[g+1][:]
   i=a.H[g]
   if i>=0:
    _k(j,e,f[i][0])
   a.Q[g]=j
  a.G+=d
def _q(a,b,c,d,e,f,g,h=None):
 if c<2:
  return g
 i,j=(a*a,b*b)
 k=_p(d,e,f,g+[-1]*(c-len(g)),i)
 if k.G==_c(d,e):
  return g
 l=random.Random(sum(((B+7)*C for B,C in enumerate(d)))+c*977+9167)
 width=a-b+1
 if h is None:
  h=min(2400,max(160,450000//i))
 for m in range(h):
  n=l.randrange(c-1)
  o=m%2
  p=k.H[n+o]
  q=l.randrange(5)
  if q<2 and p>=0:
   r,s,t=f[p][1]
   r=min(width-1,max(0,r+l.choice((-2,-1,0,0,1,2))))
   s=min(width-1,max(0,s+l.choice((-2,-1,0,0,1,2))))
   u=(r*width+s)*4+l.randrange(4)
  elif q==4:
   u=-1
  else:
   u=l.randrange(len(f))
  if o==0:
   v=k.C[n][:]
   if u>=0:
    _k(v,i,f[u][0])
   w,_=_l(v,k.Q[n+2],f,i,j,current=k.H[n+1],allow_zero=True)
   x=[u,w]
  else:
   y=k.Q[n+2][:]
   if u>=0:
    _k(y,i,f[u][0])
   z,_=_l(k.C[n],y,f,i,j,current=k.H[n],allow_zero=True)
   x=[z,u]
  if k.H[n:n+2]==x:
   continue
  A=k.m(n,x)
  if A>0 or(A==0 and l.randrange(8)==0):
   k.a(n,x,A)
   if k.G==_c(d,e):
    break
 return[B for B in k.H if B>=0]
def _r(a,b):
 if b<0:
  return 0
 c=0
 for d,e in enumerate(a.b[b][0]):
  f,g=(a.J[d],a.q[e])
  h,i=(a.Q[e],a.R[d])
  c+=(f==h)+(g==i)-(g==h)-(f==i)
 return c
def _s(a,b,c,d):
 e=_r(a,b)
 if b>=0:
  a.e(b)
 e+=_r(a,c)
 if b>=0:
  a.e(b)
 f=(b,c)
 if e<0:
  e,f=(0,(-1,-1))
 for g,h in d:
  i=_r(a,g)
  if g>=0:
   a.e(g,wishes=bool(h))
  j,k=a.f()
  if g>=0:
   a.e(g,wishes=bool(h))
  l=i+k
  if l>=e:
   e=l
   f=(j,g)if h else(g,j)
 return f
def _t(a,b,c,d,e,f,g,passes=4,width=32):
 h=a*a
 i=a-b+1
 j=random.Random(sum(((B+13)*C for B,C in enumerate(d)))+c*691+7147)
 for k in range(passes):
  g=g+[-1]*min(8,c-len(g))
  l=d[:]
  for m in g:
   if m>=0:
    _k(l,h,f[m][0])
  if sum((B==C for B,C in zip(l,e)))==_c(d,e):
   return[B for B in g if B>=0]
  n=list(range(len(f)))
  j.shuffle(n)
  o=_n(a,b,l,e,f,n)
  p=len(g)-1
  if k%2 and p>=0:
   q=g[p]
   if q>=0:
    o.e(q)
   r,_=o.f()
   g[p]=r
   if r>=0:
    o.e(r,wishes=True)
   p-=1
  while p>=1:
   s,t=(g[p-1],g[p])
   if t>=0:
    o.e(t)
   if s>=0:
    o.e(s)
   u=[(s,0),(t,1),(-1,0),(-1,1)]
   for _ in range(width):
    v=j.randrange(2)
    q=t if v else s
    w=j.randrange(4)
    if w==0 and q>=0:
     x,y,z=f[q][1]
     x=min(i-1,max(0,x+j.choice((-1,0,1))))
     y=min(i-1,max(0,y+j.choice((-1,0,1))))
     A=(x*i+y)*4+j.randrange(4)
    elif w==1:
     A=j.choice(g)
    else:
     A=j.randrange(len(f))
    u.append((A,v))
   s,t=_s(o,s,t,u)
   g[p-1],g[p]=(s,t)
   if t>=0:
    o.e(t,wishes=True)
   if s>=0:
    o.e(s,wishes=True)
   p-=2
  if p==0:
   q=g[0]
   if q>=0:
    o.e(q)
   g[0],_=o.f()
  g=[B for B in g if B>=0]
 return g
def _u(a,b,c,d,e,f,g):
 if a>16:
  return g
 h=a*a
 def i(y):
  z=d[:]
  for A in y:
   if A>=0:
    _k(z,h,f[A][0])
  return sum((B==C for B,C in zip(z,e)))
 j=i(g)
 k=_c(d,e)
 if j==k:
  return g
 l=random.Random(sum(((y+29)*z for y,z in enumerate(d)))+c*2281)
 m=g[:]
 width=a-b+1
 n=max(2,min(8,9000//(h+6*c)))
 for o in range(n):
  p=m+[-1]*min(8,c-len(m))
  q=l.sample(range(len(p)),min(len(p),2+o%6))
  for r in q:
   s=p[r]
   t=l.randrange(4)
   if s>=0 and t<2:
    u,v,w=f[s][1]
    u=max(0,min(width-1,u+l.choice((-2,-1,0,1,2))))
    v=max(0,min(width-1,v+l.choice((-2,-1,0,1,2))))
    p[r]=(u*width+v)*4+l.randrange(4)
   elif t==2:
    p[r]=-1
   else:
    p[r]=l.randrange(len(f))
  p=_o(a,b,c,d,e,f,p,passes=4,seed_offset=37307*(o+1))
  x=i(p)
  if x>=j:
   m,j=(p,x)
   if x==k:
    break
 return m
class _v(_g):
 def __init__(a,b,c,d,e,f,g,h=None):
  super().__init__(b,c,d,e,f,g,h)
  a.P=[2 if min(r//b,r%b,b-1-r//b,b-1-r%b)<c-1 else 1 for r in range(b*b)]
  a.I=2*c*c
  a.r=[[0]*d for _ in g]
  for i,j in enumerate(a.z):
   k=1<<i
   for l,m in enumerate(a.b[j][0]):
    if a.P[m]==2:
     a.r[l][f[m]]|=k
  a.i=[sum((a.P[s]for s in r if e[s]==f[s]))for r in a.F]
  a.y=[0]*6
  for n,o in enumerate(a.i):
   p=a.I-o
   for q in range(6):
    if p&1<<q:
     a.y[q]|=a.E[n]
 def o(a,b):
  return sum((a.P[d]for c,d in enumerate(a.b[b][0])if a.J[c]==a.M[d]))-a.i[b>>2]
 def e(a,b):
  c,_=a.b[b]
  d,e,f=(a.q,a.J,a.M)
  g={}
  for h,i in enumerate(c):
   j,k=(d[i],e[h])
   e[h],d[i]=(j,k)
   l=(k==f[i])-(j==f[i])
   a.u+=l
   if l:
    l*=a.P[i]
    for m in a.j[i]:
     g[m]=g.get(m,0)+l
  n,o,p=(a.i,a.y,a.E)
  q=a.I
  for m,l in g.items():
   if not l:
    continue
   j=n[m]
   k=j+l
   n[m]=k
   r=q-j^q-k
   s=p[m]
   while r:
    t=r&-r
    o[t.bit_length()-1]^=s
    r^=t
  u=a.h
  a.K=sum((1<<u*v+w for v,w in enumerate(e)))
 def g(a):
  b=[0]*6
  for c,d in enumerate(a.J):
   e=a.r[c][d]
   for f,g in((0,a.N[c][d]^e),(1,e)):
    while g:
     h=b[f]
     b[f]=h^g
     g&=h
     f+=1
  g=0
  for f in range(6):
   i,j=(b[f],a.y[f])
   k=i^j
   b[f]=k^g
   g=i&j|k&g
  l,m=(a.c,0)
  for f in range(5,-1,-1):
   n=l&b[f]
   if n:
    l=n
    m|=1<<f
  return(m-a.I,l)
def _w(a,b,c,d,e,f,g):
 h=7418729
 for i in e+f+g:
  h=(h^i)*1000003&4294967295
 j=random.Random(h)
 k=list(range(4*(a-b+1)**2))
 l=sum((z==A for z,A in zip(e,f)))
 m,n=(l,[])
 o=_c(e+g,f)
 if m==o:
  return n
 for p in range(4):
  if p:
   j.shuffle(k)
  q=_v(a,b,c,e[:],f,g[:],k[:])
  r,s,t=([],set(),l)
  for _ in range(d):
   s.add(tuple(q.J))
   u,v=q.g()
   if u<0:
    break
   w=-1
   while v:
    x=v&-v
    y=q.z[x.bit_length()-1]
    if u>0 or tuple((q.q[z]for z in q.b[y][0]))not in s:
     w=y
     break
    v^=x
   if w<0:
    break
   if u>0:
    s.clear()
   t+=sum(((q.J[z]==f[A])-(q.q[A]==f[A])for z,A in enumerate(q.b[w][0])))
   q.e(w)
   r.append(q.b[w][1])
   if t>m:
    m,n=(t,r[:])
   if m==o:
    return n
 return n
def _x(a,b,c,d,e,f,g):
 h=_c(e+g,f)
 i=sum((y==z for y,z in zip(e,f)))
 if i==h:
  return[(h,[])]
 j,k,l,m,n=_d(a,b,f)
 width=a-b+1
 o=[]
 for p in(_f,_h,_j,_w):
  q=p(a,b,c,d,e[:],f,g[:])
  r,s=(e[:],g[:])
  for t,u,v in q:
   w=(t*width+u)*4+v
   _e(r,s,j[w])
  x=sum((y==z for y,z in zip(r,f)))
  o.append((x,q))
  if x==h:
   break
 o.sort(key=lambda y:y[0],reverse=True)
 return o
def _y(a,b,c,d,e,f,g):
 h=_x(a,b,c,d,e[:],f,g[:])
 if h[0][0]==_c(e+g,f):
  return h[0][1]
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 width=a-b+1
 l=e+g
 m,n=(-1,[])
 for _,o in h[:4]:
  p=[(t*width+u)*4+v for t,u,v in o]
  p=_o(a,b,d,l,f,k,p,passes=2)
  q=l[:]
  for r in p:
   _k(q,a*a,k[r][0])
  s=sum((t==u for t,u in zip(q,f)))
  if s>m:
   m,n=(s,p)
 p=_o(a,b,d,l,f,k,n,passes=6,offset=2)
 p=_t(a,b,d,l,f,k,p)
 p=_q(a,b,d,l,f,k,p)
 p=_o(a,b,d,l,f,k,p,passes=2)
 p=_u(a,b,d,l,f,k,p)
 return[k[t][1]for t in p]
def _z(a):
 b=object.__new__(_g)
 b.__dict__=a.__dict__.copy()
 b.q=a.q[:]
 b.J=a.J[:]
 b.i=a.i[:]
 b.y=a.y[:]
 return b
def _A(a,b):
 c,d=(a.K,a.i)
 e=[(c&q).bit_count()-d[p>>2]for p,q in enumerate(a.t)]
 f=max(e)
 g=[[],[],[]]
 for h,i in enumerate(e):
  j=f-i
  if j<3:
   g[j].append(h)
 k=[]
 for l,m in zip(g,(4,3,1)):
  b.shuffle(l)
  n={}
  for h in l:
   o=tuple((a.q[p]for p in a.b[h][0]))
   if n.get(o,0)>=2:
    continue
   n[o]=n.get(o,0)+1
   k.append((h,e[h]))
   m-=1
   if m==0:
    break
 return k
def _B(a,b,c,d,e,f,g,width=24):
 h=_g(a,b,c,e[:],f,g[:])
 i=sum((I==J for I,J in zip(e,f)))
 j=[0]*c
 k=[0]*c
 for l in e+g:
  j[l]+=1
 for l in f:
  k[l]+=1
 m=sum((min(I,J)for I,J in zip(j,k)))-i
 if m<=0:
  return[]
 n=47893+d*1009+a*79+b*13+c
 for o in e+g:
  n=n*131+o&4294967295
 p=random.Random(n)
 q=[(h,0,[])]
 r,s=(0,[])
 for depth in range(d):
  t=[]
  u=set()
  for v,w,x in q:
   for y,z in _A(v,p):
    if x and y==x[-1]:
     continue
    A=_z(v)
    A.e(y)
    B=bytes(A.q)+bytes(A.J)
    if B in u:
     continue
    u.add(B)
    C=w+z
    D=x+[y]
    if C>r:
     r,s=(C,D)
     if r==m:
      return[h.b[I][1]for I in s]
    E=max(0,A.f()[0])if depth+1<d else 0
    F=C*2+E
    t.append((F,C,A,D))
  if not t:
   break
  t.sort(key=lambda I:(I[0],I[1]),reverse=True)
  q=[]
  G={}
  H=[]
  for F,w,v,x in t:
   key=tuple(v.J)
   if G.get(key,0)>=3:
    H.append((v,w,x))
    continue
   G[key]=G.get(key,0)+1
   q.append((v,w,x))
   if len(q)==width:
    break
  if len(q)<width:
   q.extend(H[:width-len(q)])
 return[h.b[I][1]for I in s]
def _C(a,b,c,d,e,f,g):
 h=_g(a,b,c,e[:],f,g[:])
 i,j=h.f()
 k,l=(max(0,i),[j]if i>0 else[])
 if d==1:
  return[h.b[s][1]for s in l]
 m=[(h.o(s),s)for s in range(len(h.b))]
 m.sort(reverse=True)
 for n,o in m:
  if n+b*b<=k:
   break
  h.e(o)
  p,q=h.f()
  r=n+p
  h.e(o)
  if r>k:
   k,l=(r,[o,q])
 return[h.b[s][1]for s in l]
def _D(a,b,c,d,e,f,g):
 if d<=2:
  return _C(a,b,c,d,e,f,g)
 h=_y(a,b,c,d,e[:],f,g[:])
 if d>24:
  return h
 i=_B(a,b,c,d,e,f,g,width=24 if d<=12 else 12)
 j,_,k,_,_=_d(a,b,f)
 l=list(zip(j,k))
 width=a-b+1
 m=[(w*width+x)*4+y for w,x,y in i]
 m=_o(a,b,d,e+g,f,l,m)
 i=[l[w][1]for w in m]
 n,o=(-1,[])
 for p in(h,i):
  q,r=(e[:],g[:])
  for s,t,u in p:
   _e(q,r,j[(s*width+t)*4+u])
  v=sum((w==x for w,x in zip(q,f)))
  if v>n:
   n,o=(v,p)
 return o
def _E(a,b,c,d,e,f):
 g=_r(a,b)
 if b>=0:
  a.e(b)
 g+=_r(a,c)
 if c>=0:
  a.e(c)
 g+=_r(a,d)
 if c>=0:
  a.e(c)
 if b>=0:
  a.e(b)
 h=(b,c,d)
 for b in e:
  i=_r(a,b)
  if b>=0:
   a.e(b)
  for d in f:
   j=_r(a,d)
   if d>=0:
    a.e(d,wishes=True)
   c,k=a.f()
   if d>=0:
    a.e(d,wishes=True)
   l=i+j+k
   if l>=g:
    g=l
    h=(b,c,d)
  if b>=0:
   a.e(b)
 return h
def _F(a,b,c,d,e,f,g,passes=2):
 if c<3:
  return g
 h=a*a
 i=_c(d,e)
 j=a-b+1
 k=random.Random(sum(((G+17)*H for G,H in enumerate(d)))+c*1777+71983)
 for l in range(passes):
  g=g+[-1]*min(6,c-len(g))
  m=d[:]
  for n in g:
   if n>=0:
    _k(m,h,f[n][0])
  if sum((G==H for G,H in zip(m,e)))==i:
   return[G for G in g if G>=0]
  o=list(range(len(f)))
  k.shuffle(o)
  p=_n(a,b,m,e,f,o)
  q=len(g)-1
  for _ in range(l%3):
   if q<0:
    break
   r=g[q]
   if r>=0:
    p.e(r)
   s,_=p.f()
   g[q]=s
   if s>=0:
    p.e(s,wishes=True)
   q-=1
  while q>=2:
   t,u,v=g[q-2:q+1]
   for n in(v,u,t):
    if n>=0:
     p.e(n)
   w,_=p.f()
   x=[]
   for r in(t,v):
    y=k.randrange(3)
    if y==0 and r>=0:
     z,A,B=f[r][1]
     z=min(j-1,max(0,z+k.choice((-1,0,1))))
     A=min(j-1,max(0,A+k.choice((-1,0,1))))
     C=(z*j+A)*4+k.randrange(4)
    elif y==1:
     D=k.randrange(h)
     for _ in range(10):
      D=k.randrange(h)
      if p.Q[D]<6 and p.q[D]!=p.Q[D]:
       break
     z=min(j-1,max(0,D//a-k.randrange(b)))
     A=min(j-1,max(0,D%a-k.randrange(b)))
     C=(z*j+A)*4+k.randrange(4)
    else:
     C=k.randrange(len(f))
    x.append(list(dict.fromkeys((r,-1,w,C))))
   for E in x[1]:
    if E>=0:
     p.e(E,wishes=True)
    F,_=p.f()
    if E>=0:
     p.e(E,wishes=True)
    if F not in x[0]:
     x[0].append(F)
   t,u,v=_E(p,t,u,v,*x)
   g[q-2:q+1]=(t,u,v)
   for n in(v,u,t):
    if n>=0:
     p.e(n,wishes=True)
   q-=3
  while q>=0:
   r=g[q]
   if r>=0:
    p.e(r)
   s,_=p.f()
   g[q]=s
   if s>=0:
    p.e(s,wishes=True)
   q-=1
  g=[G for G in g if G>=0]
 return g
def _G(a,b,c,d,e,f,g):
 h=_D(a,b,c,d,e[:],f,g[:])
 if d<=2:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 l=a-b+1
 m=[(n*l+o)*4+p for n,o,p in h]
 m=_F(a,b,d,e+g,f,k,m)
 m=_o(a,b,d,e+g,f,k,m,passes=2)
 return[k[n][1]for n in m]
def _H(a,b,c,d,e,f,g):
 if a>16 or d<=2:
  return _G(a,b,c,d,e,f,g)
 h=e+g
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 width=a-b+1
 def l(w):
  x=h[:]
  for y in w:
   _k(x,a*a,i[y])
  return sum((z==A for z,A in zip(x,f)))
 m=_i(a,b,c,d,e[:],f,g[:])
 n=[(w*width+x)*4+y for w,x,y in m]
 n=_o(a,b,d,h,f,k,n)
 n=_t(a,b,d,h,f,k,n)
 n=_q(a,b,d,h,f,k,n)
 n=_o(a,b,d,h,f,k,n,passes=2)
 o=_u(a,b,d,h,f,k,n)
 if d<=24:
  p=_B(a,b,c,d,e,f,g,width=24 if d<=12 else 12)
  p=[(w*width+x)*4+y for w,x,y in p]
  p=_o(a,b,d,h,f,k,p)
  q=l(p)
  if q>l(n):
   n=p
  if q>l(o):
   o=p
 r=[n]
 if o!=n:
  r.append(o)
 s,t=(-1,None)
 for u in r:
  u=_F(a,b,d,h,f,k,u)
  u=_o(a,b,d,h,f,k,u,passes=2)
  u=_K(a,b,d,h,f,k,u)
  u=_o(a,b,d,h,f,k,u,passes=2)
  v=l(u)
  if v>s:
   s,t=(v,u)
 return[j[w]for w in t]
def _I(a,b,c,d,e,f,g):
 h=_H(a,b,c,d,e,f,g)
 if a>6 or d<=24:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 width=a-b+1
 def l(p):
  q,r=(e[:],g[:])
  for s,t,u in p:
   _e(q,r,i[(s*width+t)*4+u])
  return sum((v==w for v,w in zip(q,f)))
 m=l(h)
 if m==_c(e+g,f):
  return h
 n=_B(a,b,c,min(d,60),e,f,g,width=96)
 o=[(p*width+q)*4+r for p,q,r in n]
 o=_o(a,b,d,e+g,f,k,o)
 o=_K(a,b,d,e+g,f,k,o)
 o=_o(a,b,d,e+g,f,k,o,passes=2)
 n=[k[p][1]for p in o]
 return n if l(n)>m else h
class _J:
 def __init__(a,b,c,d,e,f,g,h):
  a.H=g[:]
  a.b=f
  a.A=0
  a.L=_n(b,c,d,e,f,h)
  i=d[:]
  for j in g:
   if j>=0:
    _k(i,b*b,f[j][0])
  a.G=sum((k==l for k,l in zip(i,e)))
  for j in reversed(g[2:]):
   if j>=0:
    a.L.e(j,wishes=True)
 def v(a,b):
  if b>a.A:
   c=range(a.A,b)
  else:
   c=range(a.A-1,b-1,-1)
  for d in c:
   e,f=(a.H[d],a.H[d+2])
   if e>=0:
    a.L.e(e)
   if f>=0:
    a.L.e(f,wishes=True)
  a.A=b
 def D(a,b,c):
  d=a.L
  e,f=a.H[a.A:a.A+2]
  g=_r(d,e)
  if e>=0:
   d.e(e)
  g+=_r(d,f)
  if e>=0:
   d.e(e)
  h=_r(d,b)
  if b>=0:
   d.e(b,wishes=bool(c))
  i,j=d.f()
  if b>=0:
   d.e(b,wishes=bool(c))
  k=(i,b)if c else(b,i)
  return(k,h+j-g)
 def a(a,b,c):
  a.H[a.A:a.A+2]=b
  a.G+=c
def _K(a,b,c,d,e,f,g,h=None):
 import math
 if c<3:
  return g
 i=_c(d,e)
 j=d[:]
 for k in g:
  if k>=0:
   _k(j,a*a,f[k][0])
 if sum((F==G for F,G in zip(j,e)))==i:
  return[F for F in g if F>=0]
 l=random.Random(sum(((F+23)*G for F,G in enumerate(d)))+c*1357+7751)
 m=list(range(len(f)))
 l.shuffle(m)
 g=g+[-1]*(c-len(g))
 n=_J(a,b,d,e,f,g,m)
 if n.G==i:
  return[F for F in g if F>=0]
 if h is None:
  h=min(4000,max(300,900000//(a*a)))
 o,p=(n.G,n.H[:])
 q=max(1,h//4)
 r=l.randrange(c-1)
 n.v(r)
 s=1
 t=a-b+1
 for u in range(h):
  if u and u%q==0:
   l.shuffle(m)
   n=_J(a,b,d,e,f,p,m)
   r=l.randrange(c-1)
   n.v(r)
  v=u%2
  w=n.H[r+v]
  x=l.randrange(5)
  if x==0 and w>=0:
   y,z,A=f[w][1]
   y=min(t-1,max(0,y+l.choice((-2,-1,0,0,1,2))))
   z=min(t-1,max(0,z+l.choice((-2,-1,0,0,1,2))))
   B=(y*t+z)*4+l.randrange(4)
  elif x==1:
   B=n.L.f()[0]
  elif x==4:
   B=-1
  else:
   B=l.randrange(len(f))
  C,D=n.D(B,v)
  E=0.4*(1-u%q/q)**2+0.04
  if D>=0 or l.random()<math.exp(D/E):
   n.a(C,D)
   if n.G>=o:
    o,p=(n.G,n.H[:])
    if o==i:
     break
  if l.randrange(16)==0:
   s=-s
  if not 0<=r+s<c-1:
   s=-s
  r+=s
  n.v(r)
 return[F for F in p if F>=0]
def _L(a,b,c,d,e,f,g):
 h=_I(a,b,c,d,e[:],f,g[:])
 if d<=2 or a<=16:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 l=a-b+1
 m=[(n*l+o)*4+p for n,o,p in h]
 m=_K(a,b,d,e+g,f,k,m)
 m=_o(a,b,d,e+g,f,k,m,passes=2)
 return[k[n][1]for n in m]
def _M(a,b,c,d,e,f,g):
 if a==4 and b==3 and(c==2):
  h=_W(e,f,g,d,depth=5)
  if h is not None:
   return[(i//8,i//4%2,i%4)for i in h]
 return _L(a,b,c,d,e,f,g)
def _N(a,b,c=(3,)):
 d=[]
 e=[[(y,z),(z,b-1-y),(b-1-y,b-1-z),(b-1-z,y)]for y in range(b)for z in range(b)]
 for f in range(b):
  for g in range(1 if f==0 else 1-b,b):
   for h in range(4):
    i=[y[h]for y in e]
    for j in range(4):
     k=[(f+y[j][0],g+y[j][1])for y in e]
     l=set(i+k)
     m={y:y for y in l}
     m.update({y:y for y in range(b*b)})
     for n in range(2):
      o,p=(k,i)if n else(i,k)
      q=m.copy()
      for r in range(1,max(c)+1):
       for s in(o,p):
        for t,u in enumerate(s):
         q[t],q[u]=(q[u],q[t])
       if r not in c:
        continue
       v=[]
       for u in sorted(l):
        w=q[u]
        if w==u:
         continue
        x=a*a+w if isinstance(w,int)else w[0]*a+w[1]
        v.append((u[0]*a+u[1],x,isinstance(w,int)))
       if v:
        d.append((f,g,h,j,n,r,v))
 return d
def _O(a,b,c,d,e,f,g=(3,),h=3):
 if f<6:
  return[]
 i=_N(a,b,tuple((H for H in g if 2*H<=f)))
 width=a-b+1
 j=c+e
 k=[]
 for _ in range(h):
  l={H for H in range(a*a)if j[H]!=d[H]}
  if not l:
   break
  m=0
  n=None
  for o,p,q,r,s,t,u in i:
   if len(k)+2*t>f:
    continue
   if len(l)*len(u)<width*width:
    v=sorted({H-offset for H in l for offset,_,_ in u})
   else:
    v=(H*a+I for H in range(width-o)for I in range(max(0,-p),min(width,width-p)))
   for w in v:
    x,y=divmod(w,a)
    if not(0<=x<width-o and max(0,-p)<=y<min(width,width-p)):
     continue
    z=sum((w+H in l for H,_,_ in u))
    if z<=m:
     continue
    for A,B,C in u:
     D=w+A
     if j[B if C else w+B]!=d[D]:
      z-=1
      if z<=m:
       break
    if z>m:
     m=z
     E,F=((x,y,q),(x+o,y+p,r))
     n=([F,E]if s else[E,F])*t
  if n is None:
   break
  k.extend(n)
  for x,y,q in n:
   for G,offset in enumerate([((H,I),(I,b-1-H),(b-1-H,b-1-I),(b-1-I,H))[q]for H in range(b)for I in range(b)]):
    A=(x+offset[0])*a+y+offset[1]
    j[a*a+G],j[A]=(j[A],j[a*a+G])
 return k
def _P(a):
 b=[]
 for c in a:
  if b and b[-1]==c:
   b.pop()
  else:
   b.append(c)
 return b
def _Q(a,b,c,d,e,f,g=0):
 h=c[:]
 for i in f:
  _k(h,a*a,e[i][0])
 j=list(range(len(e)))
 random.Random(g).shuffle(j)
 k=_n(a,b,h,d,e,j)
 l=(0,-1,-1)
 for m in range(len(f),-1,-1):
  i,n=k.f()
  if n>l[0]:
   l=(n,m,i)
  if m:
   o=f[m-1]
   k.e(o)
   k.e(o,wishes=True)
 return l
def _R(a,b,c,d,e,f):
 g=c[:]
 for h in f:
  _k(g,a*a,e[h][0])
 i=_n(a,b,g,d,e,list(range(len(e))))
 j=[0]*len(f)
 for k in range(len(f)-1,-1,-1):
  l=f[k]
  i.e(l)
  j[k]=-_r(i,l)
  i.e(l,wishes=True)
 return j
def _S(a,b,c,d,e,f,g,h=1,i=0):
 j=a*a
 g=g[:]
 k=d[:]
 for l in g:
  _k(k,j,f[l][0])
 m=sum((y==z for y,z in zip(k,e)))
 n=_c(d,e)
 for o in range(h):
  if m==n:
   break
  p=sum(((y+11)*z for y,z in enumerate(d)))+o*10891
  q,r=(0,g)
  if len(g)<c:
   s,t,l=_Q(a,b,d,e,f,g,p)
   if s:
    q,r=(s,g[:t]+[l]+g[t:])
  if i and g:
   u=_R(a,b,d,e,f,g)
   v=sorted(range(len(g)),key=lambda y:(u[y],-y),reverse=True)
   for w in v[:i]:
    x=g[:w]+g[w+1:]
    s,t,l=_Q(a,b,d,e,f,x,p+w)
    s+=u[w]
    if s>q:
     q,r=(s,x[:t]+[l]+x[t:]if l>=0 else x)
  if q<=0:
   break
  g=r
  m+=q
 return g
def _T(a,b,c,d,e,f,g):
 h=_M(a,b,c,d,e[:],f,g[:])
 if d<=2:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=a-b+1
 l=_P([(x*k+y)*4+z for x,y,z in h])
 m=e+g
 l=_S(a,b,d,m,f,list(zip(i,j)),l,8,5)
 n=m[:]
 for o in l:
  _k(n,a*a,i[o])
 p=[j[x]for x in l]
 if sum((x==y for x,y in zip(n,f)))>=_c(m,f):
  return p
 q=min(12,max(3,3000//(a*a)))
 for r,s in[((3,),q)]+[(tuple([x]),1)for x in[6,6,9,5]]:
  if d-len(p)<2*min(r):
   continue
  t=_O(a,b,n[:a*a],f,n[a*a:],d-len(p),r,s)
  p.extend(t)
  for u,v,w in t:
   _k(n,a*a,i[(u*k+v)*4+w])
 return p
def _U():
 a=[]
 for b in range(4):
  c=[]
  for d in range(3):
   e=[]
   for f in range(512):
    g=0
    for h in range(3):
     i,j=((d,h),(h,2-d),(2-d,2-h),(2-h,d))[b]
     g|=(f>>3*h&7)<<3*(i*3+j)
    e.append(g)
   c.append(e)
  a.append(c)
 k=(1<<48)-1
 l=[]
 for i in range(2):
  for j in range(2):
   m=3*(4*i+j)
   n=k^(511|511<<12|511<<24)<<m
   l.append((m,n))
 def o(q,r):
  s=a[r]
  return s[0][q&511]|s[1][q>>9&511]|s[2][q>>18]
 def p(q):
  r,s=(q&k,q>>48)
  t=[o(s,D)for D in range(4)]
  u=[D&511|(D&261632)<<3|(D&133955584)<<6 for D in t]
  for v,(w,x)in enumerate(l):
   y=r>>w
   z=y&511|y>>3&261632|y>>6&133955584
   A=r&x
   for B in range(4):
    C=A|u[B]<<w|o(z,-B&3)<<48
    yield(v*4+B,C)
 return p
def _V(a,b):
 c=b|(1<<27)-1<<48
 d={c:b''}
 e=[c]
 for depth in range(1,5):
  f=[]
  for g in e:
   h=d[g]
   for i,j in a(g):
    if j in d:
     continue
    k=h+bytes((i,))
    d[j]=k
    f.append(j)
    wishes=j
    l=bytearray()
    for m in range(25):
     n=wishes&7
     wishes>>=3
     if n!=7:
      l.append(m*6+n)
    yield(depth,k,bytes(l))
  e=f
def _W(a,b,c,d,depth=8):
 global _Y,_Z
 if a==b:
  return[]
 if _c(a+c,b)<16:
  return None
 if _Y is None:
  _Y=_U()
 e=_Y
 f=sum((M<<3*L for L,M in enumerate(a+c)))
 g=sum((M<<3*L for L,M in enumerate(b)))
 h=(1<<48)-1
 i={f:b''}
 j=[f]
 k=min(4,d,depth)
 for _ in range(k):
  l=[]
  for m in j:
   n=i[m]
   for o,p in e(m):
    if p in i:
     continue
    q=n+bytes((o,))
    i[p]=q
    if p&h==g:
     return list(q)
    l.append(p)
  j=l
 r=min(4,d-k,depth-k)
 if r<=0:
  return None
 s=list(i)
 t=(len(s)+7)//8
 u=[[bytearray(t)for _ in range(6)]for _ in range(25)]
 for v,m in enumerate(s):
  offset,w=(v>>3,1<<(v&7))
  for x in u:
   x[m&7][offset]|=w
   m>>=3
 y=[int.from_bytes(M,'little')for L in u for M in L]
 z=[L.bit_count()for L in y]
 A=z.__getitem__
 B=(1<<len(s))-1
 if _Z is None or _Z[0]!=g:
  _Z=[g,[],_V(e,g)]
 C=_Z
 D=C[1]
 E=0
 while True:
  if E==len(D):
   if C[2]is None:
    break
   F=next(C[2],None)
   if F is None:
    C[2]=None
    break
   D.append(F)
  G,q,H=D[E]
  if G>r:
   break
  E+=1
  I=B
  for J in sorted(H,key=A):
   I&=y[J]
   if not I:
    break
  if I:
   K=s[(I&-I).bit_length()-1]
   return list(i[K]+q[::-1])
 return None
def _X(a,b,c,d,e,f,g):
 h=_T(a,b,c,d,e[:],f,g[:])
 if a!=4 or b!=3 or _c(e+g,f)<16:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(dict.fromkeys((max(0,len(h)-s)for s in(0,2,4,8,12))))
 for l in k:
  m,n=(e[:],g[:])
  for o,p,q in h[:l]:
   _e(m,n,i[(o*2+p)*4+q])
  if m==f:
   return h[:l]
  r=_W(m,f,n,d-l)
  if r is not None:
   return h[:l]+[j[s]for s in r]
 return h
_Y=None
_Z=None
def _aa():
 a=list(map(int,sys.stdin.buffer.read().split()))
 b,c,d,e=a[:4]
 f=b*b
 g=_X(b,c,d,e,a[4:4+f],a[4+f:4+2*f],a[4+2*f:])
 print(len(g))
 for h in g:
  print(*h)
if __name__=='__main__':
 _aa()
