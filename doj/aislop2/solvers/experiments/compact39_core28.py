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
 def n(a,b,width=64):
  c,d=(a.K,a.i)
  e=[(c&w).bit_count()-d[v>>2]for v,w in enumerate(a.t)]
  f=[v for v,w in enumerate(e)if w>=-2]
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
 for p in(_f,_h,_k):
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
class _j(_g):
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
def _k(a,b,c,d,e,f,g):
 h=_j(a,b,c,e,f,g)
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
def _l(a,b,c):
 for d,e in enumerate(c):
  a[b+d],a[e]=(a[e],a[b+d])
def _m(a,wishes,b,c,d,current=-1,allow_zero=False):
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
def _n(a,b,c,d,e,f,g):
 h,i=(a*a,b*b)
 j,wishes=(d+f,e+[-1]*i)
 k=[]
 for _ in range(c):
  l,m=_m(j,wishes,g,h,i)
  if m<=0:
   break
  _l(j,h,g[l][0])
  k.append(l)
 return k
_o={}
class _p:
 def __init__(a,b,c,d,e,f,g):
  h,i=(b*b,c*c)
  a.x,a.l=(h,i)
  a.q,a.J=(d[:h],d[h:])
  a.R,a.S=(e[:],[6]*i)
  a.b,a.z=(f,g)
  j=len(f)
  a.d=(1<<j)-1
  key=(b,c)
  k=_o.get(key)
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
   _o[key]=k
  a.B,a.E,a.F,a.j=k
  a.values=[[0]*7 for _ in range(i)]
  a.p=[[0]*7 for _ in range(i)]
  for u in range(i):
   v,w=(a.values[u],a.p[u])
   for r,x in enumerate(a.B[u]):
    v[a.q[r]]|=x
    w[a.R[r]]|=x
  a.O=[0]*j.bit_length()
  for y,s in enumerate(g):
   t=1<<s
   while y:
    z=y&-y
    a.O[z.bit_length()-1]|=t
    y^=z
  a.i=[sum((a.q[E]==a.R[E]for E in D))for D in a.F]
  a.y=[0]*5
  for p,A in enumerate(a.i):
   B=i-A
   for C in range(4):
    if B&1<<C:
     a.y[C]|=a.E[p]
 def e(a,b,wishes=False):
  if wishes:
   c,d,e,f=(a.R,a.S,a.p,a.q)
  else:
   c,d,e,f=(a.q,a.J,a.values,a.R)
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
   for d in(a.values[c][a.S[c]],a.p[c][a.J[c]]):
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
  m=k-a.l-sum((p==q for p,q in zip(a.J,a.S)))
  if m<0:
   return(-1,0)
  for n in reversed(a.O):
   if not j&j-1:
    break
   o=j&~n
   if o:
    j=o
  return((j&-j).bit_length()-1,m)
def _q(a,b,c,d,e,f,g,passes=8,offset=0,seed_offset=0):
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
    _l(n,h,f[o][0])
  if sum((u==v for u,v in zip(n,e)))==j:
   return[u for u in g if u>=0]
  p=list(range(len(f)))
  l.shuffle(p)
  q=_p(a,b,n,e,f,p)
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
class _r:
 def __init__(a,b,c,d,e,f):
  a.x=f
  a.b=d
  a.H=e[:]
  a.C=[b[:]]
  for g in e:
   h=a.C[-1][:]
   if g>=0:
    _l(h,f,d[g][0])
   a.C.append(h)
  a.R=[None]*(len(e)+1)
  a.R[-1]=c+[-1]*(len(b)-f)
  for i in range(len(e)-1,-1,-1):
   j=a.R[i+1][:]
   if e[i]>=0:
    _l(j,f,d[e[i]][0])
   a.R[i]=j
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
    _l(f,d,j)
  k=a.C[b+len(c)]
  wishes=a.R[b+len(c)]
  return sum(((f[l]==wishes[l])-(k[l]==wishes[l])for l in g))
 def a(a,b,c,d):
  e,f=(a.x,a.b)
  a.H[b:b+len(c)]=c
  for g in range(b,len(a.H)):
   h=a.C[g][:]
   i=a.H[g]
   if i>=0:
    _l(h,e,f[i][0])
   a.C[g+1]=h
  for g in range(b+len(c)-1,-1,-1):
   j=a.R[g+1][:]
   i=a.H[g]
   if i>=0:
    _l(j,e,f[i][0])
   a.R[g]=j
  a.G+=d
def _s(a,b,c,d,e,f,g,h=None):
 if c<2:
  return g
 i,j=(a*a,b*b)
 k=_r(d,e,f,g+[-1]*(c-len(g)),i)
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
    _l(v,i,f[u][0])
   w,_=_m(v,k.R[n+2],f,i,j,current=k.H[n+1],allow_zero=True)
   x=[u,w]
  else:
   y=k.R[n+2][:]
   if u>=0:
    _l(y,i,f[u][0])
   z,_=_m(k.C[n],y,f,i,j,current=k.H[n],allow_zero=True)
   x=[z,u]
  if k.H[n:n+2]==x:
   continue
  A=k.m(n,x)
  if A>0 or(A==0 and l.randrange(8)==0):
   k.a(n,x,A)
   if k.G==_c(d,e):
    break
 return[B for B in k.H if B>=0]
def _t(a,b):
 if b<0:
  return 0
 c=0
 for d,e in enumerate(a.b[b][0]):
  f,g=(a.J[d],a.q[e])
  h,i=(a.R[e],a.S[d])
  c+=(f==h)+(g==i)-(g==h)-(f==i)
 return c
def _u(a,b,c,d):
 e=_t(a,b)
 if b>=0:
  a.e(b)
 e+=_t(a,c)
 if b>=0:
  a.e(b)
 f=(b,c)
 if e<0:
  e,f=(0,(-1,-1))
 for g,h in d:
  i=_t(a,g)
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
def _v(a,b,c,d,e,f,g,passes=4,width=32):
 h=a*a
 i=a-b+1
 j=random.Random(sum(((B+13)*C for B,C in enumerate(d)))+c*691+7147)
 for k in range(passes):
  g=g+[-1]*min(8,c-len(g))
  l=d[:]
  for m in g:
   if m>=0:
    _l(l,h,f[m][0])
  if sum((B==C for B,C in zip(l,e)))==_c(d,e):
   return[B for B in g if B>=0]
  n=list(range(len(f)))
  j.shuffle(n)
  o=_p(a,b,l,e,f,n)
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
   s,t=_u(o,s,t,u)
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
def _w(a,b,c,d,e,f,g):
 if a>16:
  return g
 h=a*a
 def i(y):
  z=d[:]
  for A in y:
   if A>=0:
    _l(z,h,f[A][0])
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
  p=_q(a,b,c,d,e,f,p,passes=4,seed_offset=37307*(o+1))
  x=i(p)
  if x>=j:
   m,j=(p,x)
   if x==k:
    break
 return m
class _x(_g):
 def __init__(a,b,c,d,e,f,g,h=None):
  super().__init__(b,c,d,e,f,g,h)
  a.Q=[2 if min(r//b,r%b,b-1-r//b,b-1-r%b)<c-1 else 1 for r in range(b*b)]
  a.I=2*c*c
  a.r=[[0]*d for _ in g]
  for i,j in enumerate(a.z):
   k=1<<i
   for l,m in enumerate(a.b[j][0]):
    if a.Q[m]==2:
     a.r[l][f[m]]|=k
  a.i=[sum((a.Q[s]for s in r if e[s]==f[s]))for r in a.F]
  a.y=[0]*6
  for n,o in enumerate(a.i):
   p=a.I-o
   for q in range(6):
    if p&1<<q:
     a.y[q]|=a.E[n]
 def o(a,b):
  return sum((a.Q[d]for c,d in enumerate(a.b[b][0])if a.J[c]==a.M[d]))-a.i[b>>2]
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
    l*=a.Q[i]
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
def _y(a,b,c,d,e,f,g):
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
  q=_x(a,b,c,e[:],f,g[:],k[:])
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
def _z(a,b,c,d,e,f,g):
 h=_c(e+g,f)
 i=sum((y==z for y,z in zip(e,f)))
 if i==h:
  return[(h,[])]
 j,k,l,m,n=_d(a,b,f)
 width=a-b+1
 o=[]
 for p in(_f,_h,_k,_y):
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
def _A(a,b,c,d,e,f,g):
 h=_z(a,b,c,d,e[:],f,g[:])
 if h[0][0]==_c(e+g,f):
  return h[0][1]
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 width=a-b+1
 l=e+g
 m,n=(-1,[])
 for _,o in h[:4]:
  p=[(t*width+u)*4+v for t,u,v in o]
  p=_q(a,b,d,l,f,k,p,passes=2)
  q=l[:]
  for r in p:
   _l(q,a*a,k[r][0])
  s=sum((t==u for t,u in zip(q,f)))
  if s>m:
   m,n=(s,p)
 p=_q(a,b,d,l,f,k,n,passes=6,offset=2)
 p=_v(a,b,d,l,f,k,p)
 p=_s(a,b,d,l,f,k,p)
 p=_q(a,b,d,l,f,k,p,passes=2)
 p=_w(a,b,d,l,f,k,p)
 return[k[t][1]for t in p]
def _B(a):
 b=object.__new__(_g)
 b.__dict__=a.__dict__.copy()
 b.q=a.q[:]
 b.J=a.J[:]
 b.i=a.i[:]
 b.y=a.y[:]
 return b
def _C(a,b):
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
def _D(a,b,c,d,e,f,g,width=24):
 h=_g(a,b,c,e[:],f,g[:])
 i=sum((J==K for J,K in zip(e,f)))
 j=[0]*c
 k=[0]*c
 for l in e+g:
  j[l]+=1
 for l in f:
  k[l]+=1
 m=sum((min(J,K)for J,K in zip(j,k)))-i
 if m<=0:
  return[]
 n=47893+d*1009+a*79+b*13+c
 for o in e+g:
  n=n*131+o&4294967295
 p=random.Random(n)
 q=[(h,0,[])]
 r,s=(0,[])
 for t in range(d):
  u=[]
  v=set()
  for w,x,y in q:
   for z,A in _C(w,p):
    if y and z==y[-1]:
     continue
    B=_B(w)
    B.e(z)
    C=bytes(B.q)+bytes(B.J)
    if C in v:
     continue
    v.add(C)
    D=x+A
    E=y+[z]
    if D>r:
     r,s=(D,E)
     if r==m:
      return[h.b[J][1]for J in s]
    F=max(0,B.f()[0])if t+1<d else 0
    G=D*2+F
    u.append((G,D,B,E))
  if not u:
   break
  u.sort(key=lambda J:(J[0],J[1]),reverse=True)
  q=[]
  H={}
  I=[]
  for G,x,w,y in u:
   key=tuple(w.J)
   if H.get(key,0)>=3:
    I.append((w,x,y))
    continue
   H[key]=H.get(key,0)+1
   q.append((w,x,y))
   if len(q)==width:
    break
  if len(q)<width:
   q.extend(I[:width-len(q)])
 return[h.b[J][1]for J in s]
def _E(a,b,c,d,e,f,g):
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
def _F(a,b,c,d,e,f,g):
 if d<=2:
  return _E(a,b,c,d,e,f,g)
 h=_A(a,b,c,d,e[:],f,g[:])
 if d>24:
  return h
 i=_D(a,b,c,d,e,f,g,width=24 if d<=12 else 12)
 j,_,k,_,_=_d(a,b,f)
 l=list(zip(j,k))
 width=a-b+1
 m=[(w*width+x)*4+y for w,x,y in i]
 m=_q(a,b,d,e+g,f,l,m)
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
def _G(a,b,c,d,e,f):
 g=_t(a,b)
 if b>=0:
  a.e(b)
 g+=_t(a,c)
 if c>=0:
  a.e(c)
 g+=_t(a,d)
 if c>=0:
  a.e(c)
 if b>=0:
  a.e(b)
 h=(b,c,d)
 for b in e:
  i=_t(a,b)
  if b>=0:
   a.e(b)
  for d in f:
   j=_t(a,d)
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
def _H(a,b,c,d,e,f,g,passes=2):
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
    _l(m,h,f[n][0])
  if sum((G==H for G,H in zip(m,e)))==i:
   return[G for G in g if G>=0]
  o=list(range(len(f)))
  k.shuffle(o)
  p=_p(a,b,m,e,f,o)
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
      if p.R[D]<6 and p.q[D]!=p.R[D]:
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
   t,u,v=_G(p,t,u,v,*x)
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
def _I(a,b,c,d,e,f,g):
 h=_F(a,b,c,d,e[:],f,g[:])
 if d<=2:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 l=a-b+1
 m=[(n*l+o)*4+p for n,o,p in h]
 m=_H(a,b,d,e+g,f,k,m)
 m=_q(a,b,d,e+g,f,k,m,passes=2)
 return[k[n][1]for n in m]
def _J(a,b,c,d,e,f,g):
 if a>16 or d<=2:
  return _I(a,b,c,d,e,f,g)
 h=e+g
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 width=a-b+1
 def l(w):
  x=h[:]
  for y in w:
   _l(x,a*a,i[y])
  return sum((z==A for z,A in zip(x,f)))
 m=_i(a,b,c,d,e[:],f,g[:])
 n=[(w*width+x)*4+y for w,x,y in m]
 n=_q(a,b,d,h,f,k,n)
 n=_v(a,b,d,h,f,k,n)
 n=_s(a,b,d,h,f,k,n)
 n=_q(a,b,d,h,f,k,n,passes=2)
 o=_w(a,b,d,h,f,k,n)
 if d<=24:
  p=_D(a,b,c,d,e,f,g,width=24 if d<=12 else 12)
  p=[(w*width+x)*4+y for w,x,y in p]
  p=_q(a,b,d,h,f,k,p)
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
  u=_H(a,b,d,h,f,k,u)
  u=_q(a,b,d,h,f,k,u,passes=2)
  u=_M(a,b,d,h,f,k,u)
  u=_q(a,b,d,h,f,k,u,passes=2)
  v=l(u)
  if v>s:
   s,t=(v,u)
 return[j[w]for w in t]
def _K(a,b,c,d,e,f,g):
 h=_J(a,b,c,d,e,f,g)
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
 n=_D(a,b,c,min(d,60),e,f,g,width=96)
 o=[(p*width+q)*4+r for p,q,r in n]
 o=_q(a,b,d,e+g,f,k,o)
 o=_M(a,b,d,e+g,f,k,o)
 o=_q(a,b,d,e+g,f,k,o,passes=2)
 n=[k[p][1]for p in o]
 return n if l(n)>m else h
class _L:
 def __init__(a,b,c,d,e,f,g,h):
  a.H=g[:]
  a.b=f
  a.A=0
  a.L=_p(b,c,d,e,f,h)
  i=d[:]
  for j in g:
   if j>=0:
    _l(i,b*b,f[j][0])
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
  g=_t(d,e)
  if e>=0:
   d.e(e)
  g+=_t(d,f)
  if e>=0:
   d.e(e)
  h=_t(d,b)
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
def _M(a,b,c,d,e,f,g,h=None):
 import math
 if c<3:
  return g
 i=_c(d,e)
 j=d[:]
 for k in g:
  if k>=0:
   _l(j,a*a,f[k][0])
 if sum((F==G for F,G in zip(j,e)))==i:
  return[F for F in g if F>=0]
 l=random.Random(sum(((F+23)*G for F,G in enumerate(d)))+c*1357+7751)
 m=list(range(len(f)))
 l.shuffle(m)
 g=g+[-1]*(c-len(g))
 n=_L(a,b,d,e,f,g,m)
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
   n=_L(a,b,d,e,f,p,m)
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
def _N(a,b,c,d,e,f,g):
 h=_K(a,b,c,d,e[:],f,g[:])
 if d<=2 or a<=16:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 l=a-b+1
 m=[(n*l+o)*4+p for n,o,p in h]
 m=_M(a,b,d,e+g,f,k,m)
 m=_q(a,b,d,e+g,f,k,m,passes=2)
 return[k[n][1]for n in m]
def _O():
 a=[]
 for b in range(4):
  c=[]
  for d in range(512):
   e=0
   for f in range(3):
    for g in range(3):
     h,i=((f,g),(g,2-f),(2-f,2-g),(2-g,f))[b]
     e|=(d>>f*3+g&1)<<h*3+i
   c.append(e)
  a.append(c)
 j=[]
 for h in range(2):
  for i in range(2):
   k=4*h+i
   l=[(o&7)<<k|(o&56)<<k+1|(o&448)<<k+2 for o in range(512)]
   m=[[l[p]for p in a[o]]for o in range(4)]
   j.append((k,65535^l[511],m))
 def n(o):
  p,q=(o&65535,o>>16)
  for r,(s,t,u)in enumerate(j):
   v=p>>s&7|p>>s+1&56|p>>s+2&448
   w=p&t
   for x in range(4):
    y=w|u[x][q]|a[-x&3][v]<<16
    yield(r*4+x,y)
 return n
def _P(a,b,c,d):
 e=sum((u<<t for t,u in enumerate(a+c)))
 f=sum((u<<t for t,u in enumerate(b)))
 if e&65535==f:
  return[]
 g=e.bit_count()-f.bit_count()
 if not 0<=g<=9:
  return None
 h=_O()
 i={e:(None,None)}
 j=[e]
 k=min(3,d)
 def l(t):
  u=[]
  while i[t][0]is not None:
   t,v=i[t]
   u.append(v)
  return u[::-1]
 for _ in range(k):
  m=[]
  for n in j:
   for o,p in h(n):
    if p in i:
     continue
    i[p]=(n,o)
    if p&65535==f:
     return l(p)
    m.append(p)
  j=m
 q=[f|t<<16 for t in range(512)if t.bit_count()==g]
 r={t:(None,None)for t in q}
 j=q
 for _ in range(min(2,d-k)):
  m=[]
  for n in j:
   for o,p in h(n):
    if p in r:
     continue
    r[p]=(n,o)
    if p in i:
     s=l(p)
     while r[p][0]is not None:
      p,o=r[p]
      s.append(o)
     return s
    m.append(p)
  j=m
 return None
def _Q(a,b,c,d,e,f,g):
 if a==4 and b==3 and(c==2):
  h=_P(e,f,g,d)
  if h is not None:
   return[(i//8,i//4%2,i%4)for i in h]
 return _N(a,b,c,d,e,f,g)
class _R:
 def __init__(a,b,c,d,e,f,g,h):
  i,j=(b*b,c*c)
  a.x,a.l=(i,j)
  a.q,a.J=(d[:i],d[i:])
  a.R,a.S=(e[:],[6]*j)
  a.Q,a.T=(f[:],[0]*j)
  a.b,a.z=(g,h)
  a.d=(1<<len(g))-1
  key=(b,c)
  k=_o.get(key)
  if k is None:
   l=[[0]*i for _ in range(j)]
   m=[15<<4*E for E in range(len(g)//4)]
   n=[g[E][0]for E in range(0,len(g),4)]
   o=[[]for _ in range(i)]
   for p,q in enumerate(n):
    for r in q:
     o[r].append(p)
   for s,(q,_)in enumerate(g):
    t=1<<s
    for u,r in enumerate(q):
     l[u][r]|=t
   k=(l,m,n,o)
   _o[key]=k
  a.B,a.E,a.F,a.j=k
  a.values=[[0]*7 for _ in range(j)]
  a.p=[[0]*7 for _ in range(j)]
  a.P=[[0]*3 for _ in range(j)]
  for u in range(j):
   v,w,x=(a.values[u],a.p[u],a.P[u])
   for r,y in enumerate(a.B[u]):
    v[a.q[r]]|=y
    w[a.R[r]]|=y
    x[a.Q[r]]|=y
  a.O=[0]*len(g).bit_length()
  for z,s in enumerate(h):
   t=1<<s
   while z:
    A=z&-z
    a.O[A.bit_length()-1]|=t
    z^=A
  a.i=[sum((a.Q[F]*(a.q[F]==a.R[F])for F in E))for E in a.F]
  a.y=[0]*6
  for p,B in enumerate(a.i):
   C=2*j-B
   for D in range(5):
    if C&1<<D:
     a.y[D]|=a.E[p]
 def e(a,b,wishes=False):
  c={}
  d,e,f=(a.B,a.j,a.i)
  if wishes:
   g,h=(a.R,a.S)
   i,j=(a.Q,a.T)
   for k,l in enumerate(a.b[b][0]):
    m,n=(g[l],h[k])
    o,p=(i[l],j[k])
    if m!=n:
     for q in range(a.l):
      r=d[q][l]
      a.p[q][m]^=r
      a.p[q][n]^=r
    if o!=p:
     for q in range(a.l):
      r=d[q][l]
      a.P[q][o]^=r
      a.P[q][p]^=r
    s=a.q[l]
    t=p*(s==n)-o*(s==m)
    if t:
     for u in e[l]:
      c[u]=c.get(u,0)+t
    h[k],g[l]=(m,n)
    j[k],i[l]=(o,p)
  else:
   g,h=(a.q,a.J)
   for k,l in enumerate(a.b[b][0]):
    m,n=(g[l],h[k])
    if m==n:
     continue
    for q in range(a.l):
     r=d[q][l]
     a.values[q][m]^=r
     a.values[q][n]^=r
    t=a.Q[l]*((n==a.R[l])-(m==a.R[l]))
    if t:
     for u in e[l]:
      c[u]=c.get(u,0)+t
    h[k],g[l]=(m,n)
  for u,t in c.items():
   if not t:
    continue
   v=f[u]
   f[u]+=t
   w=2*a.l-v^2*a.l-f[u]
   while w:
    x=w&-w
    a.y[x.bit_length()-1]^=a.E[u]
    w^=x
 def f(a):
  b=[0]*6
  for c in range(a.l):
   d=a.p[c][a.J[c]]
   e=[(d&a.P[c][1],0),(d&a.P[c][2],1)]
   f=a.T[c]
   if f:
    e.append((a.values[c][a.S[c]],f-1))
   for g,h in e:
    while g:
     i=b[h]
     b[h]=i^g
     g&=i
     h+=1
  g=0
  for h in range(6):
   j,k=(b[h],a.y[h])
   l=j^k
   b[h]=l^g
   g=j&k|l&g
  m,n=(a.d,0)
  for h in range(5,-1,-1):
   o=m&b[h]
   if o:
    m=o
    n|=1<<h
  p=sum((t*(u==v)for t,u,v in zip(a.T,a.J,a.S)))
  q=n-2*a.l-p
  if q<0:
   return(-1,0)
  for r in reversed(a.O):
   if not m&m-1:
    break
   s=m&~r
   if s:
    m=s
  return((m&-m).bit_length()-1,q)
def _S(a,b,c,d,e,f,g,h,passes=1):
 i,j=(a*a,b*b)
 k=sum(((u+1)*v for u,v in enumerate(d)))+c*131
 k+=sum(((u+7)*v for u,v in enumerate(f)))*17
 l=random.Random(k)
 for m in range(passes):
  h=h+[-1]*min(8,c-len(h))
  n=d[:]
  for o in h:
   if o>=0:
    _l(n,i,g[o][0])
  if all((u==v for u,v in zip(n,e))):
   return[u for u in h if u>=0]
  p=list(range(len(g)))
  l.shuffle(p)
  q=_R(a,b,n,e,f,g,p)
  for r in range(len(h)-1,-1,-1):
   s=h[r]
   if s>=0:
    q.e(s)
   t,_=q.f()
   h[r]=t
   if t>=0:
    q.e(t,wishes=True)
  h=[u for u in h if u>=0]
 return h
def _T(a,b,c,d,e,f,g):
 h=_Q(a,b,c,d,e[:],f,g[:])
 if d<=2:
  return h
 i,j=(a*a,b*b)
 k,_,l,_,_=_d(a,b,f)
 m=list(zip(k,l))
 n=a-b+1
 o=[(H*n+I)*4+J for H,I,J in h]
 p,q=(e+g,e+g)
 for r in o:
  _l(q,i,k[r])
 s=sum((H==I for H,I in zip(q,f)))
 t=o
 u,v=([0]*c,[0]*c)
 for w in p:
  u[w]+=1
 for w in f:
  v[w]+=1
 x=sum((min(H,I)for H,I in zip(u,v)))
 if s==x:
  return h
 y=[min(H,a-b)-max(0,H-b+1)+1 for H in range(a)]
 z=max(y)**2
 A=[1+(y[H]*y[I]<z)for H in range(a)for I in range(a)]
 B=[1+(H!=I)for H,I in zip(q,f)]
 C=set()
 for D in(B,A):
  E=tuple(D)
  if min(D)==max(D)or E in C:
   continue
  C.add(E)
  F=_S(a,b,d,p,f,D,m,o)
  F=_q(a,b,d,p,f,m,F,passes=2)
  q=p[:]
  for r in F:
   _l(q,i,k[r])
  G=sum((H==I for H,I in zip(q,f)))
  if G>s:
   s,t=(G,F)
   if G==x:
    break
 return[l[H]for H in t]
def _U():
 a=list(map(int,sys.stdin.buffer.read().split()))
 b,c,d,e=a[:4]
 f=b*b
 g=_T(b,c,d,e,a[4:4+f],a[4+f:4+2*f],a[4+2*f:])
 print(len(g))
 for h in g:
  print(*h)
if __name__=='__main__':
 _U()
