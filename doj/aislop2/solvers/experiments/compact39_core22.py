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
   t.add(tuple(q.I))
   v,w=q.g()
   if v<0 or(v==0 and(not _b or p==0)):
    break
   x=-1
   while w:
    y=w&-w
    z=q.y[y.bit_length()-1]
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
 def __init__(a,b,c,d,e,f,g,h=None):
  a.v,a.k,a.h=(b,c,d)
  a.q,a.L,a.I=(e,f,g)
  a.t=sum((B==C for B,C in zip(e,f)))
  a.r=_c(e+g,f)
  a.E=[]
  a.b=[]
  a.s=[]
  a.j=[[]for _ in e]
  i=[]
  for j in range(4):
   k=[]
   for l in range(c):
    for m in range(c):
     n,o=((l,m),(m,c-1-l),(c-1-l,c-1-m),(c-1-m,l))[j]
     k.append(n*b+o)
   i.append(k)
  for p in range(b-c+1):
   for q in range(b-c+1):
    r=p*b+q
    s=tuple((r+B for B in i[0]))
    t=len(a.E)
    a.E.append(s)
    for n in s:
     a.j[n].append(t)
    for j in range(4):
     s=tuple((r+B for B in i[j]))
     a.b.append((s,(p,q,j)))
     a.s.append(sum((1<<d*B+f[C]for B,C in enumerate(s))))
  a.y=list(range(len(a.b)))if h is None else h
  a.i=[sum((e[C]==f[C]for C in B))for B in a.E]
  a.J=sum((1<<d*B+C for B,C in enumerate(g)))
  a.H=c*c
  a.c=(1<<len(a.b))-1
  a.M=[[0]*d for _ in g]
  a.D=[0]*len(a.E)
  for u,v in enumerate(a.y):
   w=1<<u
   a.D[v>>2]|=w
   for x,n in enumerate(a.b[v][0]):
    a.M[x][f[n]]|=w
  a.x=[0]*4
  for t,y in enumerate(a.i):
   z=a.H-y
   for A in range(4):
    if z&1<<A:
     a.x[A]|=a.D[t]
 def o(a,b):
  return(a.J&a.s[b]).bit_count()-a.i[b>>2]
 def e(a,b):
  c,_=a.b[b]
  d,e,f=(a.q,a.I,a.L)
  g={}
  for h,i in enumerate(c):
   j,k=(d[i],e[h])
   e[h],d[i]=(j,k)
   l=(k==f[i])-(j==f[i])
   a.t+=l
   if l:
    for m in a.j[i]:
     g[m]=g.get(m,0)+l
  n,o,p=(a.i,a.x,a.D)
  q=a.H
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
  a.J=sum((1<<u*v+w for v,w in enumerate(e)))
 def g(a):
  b=[0]*5
  for c,d in enumerate(a.I):
   e=a.M[c][d]
   f=0
   while e:
    g=b[f]
    b[f]=g^e
    e&=g
    f+=1
  e=0
  for f in range(4):
   h,i=(b[f],a.x[f])
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
  return(l-a.H,k)
 def f(a):
  b,c=a.g()
  d=(c&-c).bit_length()-1
  return(b,a.y[d])
 def n(a,b,width=64):
  c,d=(a.J,a.i)
  e=[(c&w).bit_count()-d[v>>2]for v,w in enumerate(a.s)]
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
  while len(p)<d and o.t<o.r:
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
  if j==o.r:
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
  c,d=(a.J,a.i)
  e=[(c&w).bit_count()-d[v>>2]for v,w in enumerate(a.s)]
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
 while len(l)<d and h.t<h.r:
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
class _o:
 def __init__(a,b,c,d,e,f,g):
  h,i=(b*b,c*c)
  a.w,a.l=(h,i)
  a.q,a.I=(d[:h],d[h:])
  a.N,a.O=(e[:],[6]*i)
  a.b,a.y=(f,g)
  a.d=(1<<len(f))-1
  a.A=[[0]*h for _ in range(i)]
  a.values=[[0]*7 for _ in range(i)]
  a.p=[[0]*7 for _ in range(i)]
  a.D=[0]*(len(f)//4)
  a.E=[f[t][0]for t in range(0,len(f),4)]
  a.j=[[]for _ in range(h)]
  for j,k in enumerate(a.E):
   for l in k:
    a.j[l].append(j)
  for m,n in enumerate(g):
   o=1<<m
   a.D[n>>2]|=o
   for p,l in enumerate(f[n][0]):
    a.A[p][l]|=o
    a.values[p][a.q[l]]|=o
    a.p[p][a.N[l]]|=o
  a.i=[sum((a.q[u]==a.N[u]for u in t))for t in a.E]
  a.x=[0]*5
  for j,q in enumerate(a.i):
   r=i-q
   for s in range(4):
    if r&1<<s:
     a.x[s]|=a.D[j]
 def e(a,b,wishes=False):
  if wishes:
   c,d,e,f=(a.N,a.O,a.p,a.q)
  else:
   c,d,e,f=(a.q,a.I,a.values,a.N)
  g=a.i[:]
  h=set()
  i,j,k=(a.A,a.j,a.i)
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
    a.x[u.bit_length()-1]^=a.D[s]
    t^=u
 def f(a):
  b=[0]*5
  for c in range(a.l):
   for d in(a.values[c][a.O[c]],a.p[c][a.I[c]]):
    e=0
    while d:
     f=b[e]
     b[e]=f^d
     d&=f
     e+=1
  d=0
  for e in range(5):
   g,h=(b[e],a.x[e])
   i=g^h
   b[e]=i^d
   d=g&h|i&d
  j,k=(a.d,0)
  for e in range(4,-1,-1):
   l=j&b[e]
   if l:
    j=l
    k|=1<<e
  m=k-a.l-sum((o==p for o,p in zip(a.I,a.O)))
  if m<0:
   return(-1,0)
  n=(j&-j).bit_length()-1
  return(a.y[n],m)
def _p(a,b,c,d,e,f,g,passes=8,seed_offset=0):
 h,i=(a*a,b*b)
 j=_c(d,e)
 k=sum(((u+1)*v for u,v in enumerate(d)))+c*131+seed_offset
 l=random.Random(k)
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
  q=_o(a,b,n,e,f,p)
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
class _q:
 def __init__(a,b,c,d,e,f):
  a.w=f
  a.b=d
  a.G=e[:]
  a.B=[b[:]]
  for g in e:
   h=a.B[-1][:]
   if g>=0:
    _l(h,f,d[g][0])
   a.B.append(h)
  a.N=[None]*(len(e)+1)
  a.N[-1]=c+[-1]*(len(b)-f)
  for i in range(len(e)-1,-1,-1):
   j=a.N[i+1][:]
   if e[i]>=0:
    _l(j,f,d[e[i]][0])
   a.N[i]=j
  a.F=sum((k==l for k,l in zip(a.B[-1],c)))
 def m(a,b,c):
  d,e=(a.w,a.b)
  f=a.B[b][:]
  g=set(range(d,len(f)))
  for h,i in zip(a.G[b:b+len(c)],c):
   if h>=0:
    g.update(e[h][0])
   if i>=0:
    j=e[i][0]
    g.update(j)
    _l(f,d,j)
  k=a.B[b+len(c)]
  wishes=a.N[b+len(c)]
  return sum(((f[l]==wishes[l])-(k[l]==wishes[l])for l in g))
 def a(a,b,c,d):
  e,f=(a.w,a.b)
  a.G[b:b+len(c)]=c
  for g in range(b,len(a.G)):
   h=a.B[g][:]
   i=a.G[g]
   if i>=0:
    _l(h,e,f[i][0])
   a.B[g+1]=h
  for g in range(b+len(c)-1,-1,-1):
   j=a.N[g+1][:]
   i=a.G[g]
   if i>=0:
    _l(j,e,f[i][0])
   a.N[g]=j
  a.F+=d
def _r(a,b,c,d,e,f,g,h=None):
 if c<2:
  return g
 i,j=(a*a,b*b)
 k=_q(d,e,f,g+[-1]*(c-len(g)),i)
 if k.F==_c(d,e):
  return g
 l=random.Random(sum(((B+7)*C for B,C in enumerate(d)))+c*977+9167)
 width=a-b+1
 if h is None:
  h=min(2400,max(160,450000//i))
 for m in range(h):
  n=l.randrange(c-1)
  o=m%2
  p=k.G[n+o]
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
   v=k.B[n][:]
   if u>=0:
    _l(v,i,f[u][0])
   w,_=_m(v,k.N[n+2],f,i,j,current=k.G[n+1],allow_zero=True)
   x=[u,w]
  else:
   y=k.N[n+2][:]
   if u>=0:
    _l(y,i,f[u][0])
   z,_=_m(k.B[n],y,f,i,j,current=k.G[n],allow_zero=True)
   x=[z,u]
  if k.G[n:n+2]==x:
   continue
  A=k.m(n,x)
  if A>0 or(A==0 and l.randrange(8)==0):
   k.a(n,x,A)
   if k.F==_c(d,e):
    break
 return[B for B in k.G if B>=0]
def _s(a,b):
 if b<0:
  return 0
 c=0
 for d,e in enumerate(a.b[b][0]):
  f,g=(a.I[d],a.q[e])
  h,i=(a.N[e],a.O[d])
  c+=(f==h)+(g==i)-(g==h)-(f==i)
 return c
def _t(a,b,c,d):
 e=_s(a,b)
 if b>=0:
  a.e(b)
 e+=_s(a,c)
 if b>=0:
  a.e(b)
 f=(b,c)
 if e<0:
  e,f=(0,(-1,-1))
 for g,h in d:
  i=_s(a,g)
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
def _u(a,b,c,d,e,f,g,passes=4,width=32):
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
  o=_o(a,b,l,e,f,n)
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
   s,t=_t(o,s,t,u)
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
def _v(a,b,c,d,e,f,g):
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
  p=_p(a,b,c,d,e,f,p,passes=4,seed_offset=37307*(o+1))
  x=i(p)
  if x>=j:
   m,j=(p,x)
   if x==k:
    break
 return m
def _w(a,b,c,d,e,f,g):
 h=_i(a,b,c,d,e[:],f,g[:])
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 width=a-b+1
 l=[(m*width+n)*4+o for m,n,o in h]
 l=_p(a,b,d,e+g,f,k,l)
 l=_u(a,b,d,e+g,f,k,l)
 l=_r(a,b,d,e+g,f,k,l)
 l=_p(a,b,d,e+g,f,k,l,passes=2)
 l=_v(a,b,d,e+g,f,k,l)
 return[k[m][1]for m in l]
def _x(a):
 b=object.__new__(_g)
 b.__dict__=a.__dict__.copy()
 b.q=a.q[:]
 b.I=a.I[:]
 b.i=a.i[:]
 b.x=a.x[:]
 return b
def _y(a,b):
 c,d=(a.J,a.i)
 e=[(c&q).bit_count()-d[p>>2]for p,q in enumerate(a.s)]
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
def _z(a,b,c,d,e,f,g,width=24):
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
   for z,A in _y(w,p):
    if y and z==y[-1]:
     continue
    B=_x(w)
    B.e(z)
    C=bytes(B.q)+bytes(B.I)
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
   key=tuple(w.I)
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
def _A(a,b,c,d,e,f,g):
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
def _B(a,b,c,d,e,f,g):
 if d<=2:
  return _A(a,b,c,d,e,f,g)
 h=_w(a,b,c,d,e[:],f,g[:])
 if d>24:
  return h
 i=_z(a,b,c,d,e,f,g,width=24 if d<=12 else 12)
 j,_,k,_,_=_d(a,b,f)
 l=list(zip(j,k))
 width=a-b+1
 m=[(w*width+x)*4+y for w,x,y in i]
 m=_p(a,b,d,e+g,f,l,m)
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
def _C(a,b,c,d,e,f):
 g=_s(a,b)
 if b>=0:
  a.e(b)
 g+=_s(a,c)
 if c>=0:
  a.e(c)
 g+=_s(a,d)
 if c>=0:
  a.e(c)
 if b>=0:
  a.e(b)
 h=(b,c,d)
 for b in e:
  i=_s(a,b)
  if b>=0:
   a.e(b)
  for d in f:
   j=_s(a,d)
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
def _D(a,b,c,d,e,f,g,passes=2):
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
  p=_o(a,b,m,e,f,o)
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
      if p.N[D]<6 and p.q[D]!=p.N[D]:
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
   t,u,v=_C(p,t,u,v,*x)
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
def _E(a,b,c,d,e,f,g):
 h=_B(a,b,c,d,e[:],f,g[:])
 if d<=2:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 l=a-b+1
 m=[(n*l+o)*4+p for n,o,p in h]
 m=_D(a,b,d,e+g,f,k,m)
 m=_p(a,b,d,e+g,f,k,m,passes=2)
 return[k[n][1]for n in m]
def _F(a,b,c,d,e,f,g):
 if a>16 or d<=2:
  return _E(a,b,c,d,e,f,g)
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
 n=_p(a,b,d,h,f,k,n)
 n=_u(a,b,d,h,f,k,n)
 n=_r(a,b,d,h,f,k,n)
 n=_p(a,b,d,h,f,k,n,passes=2)
 o=_v(a,b,d,h,f,k,n)
 if d<=24:
  p=_z(a,b,c,d,e,f,g,width=24 if d<=12 else 12)
  p=[(w*width+x)*4+y for w,x,y in p]
  p=_p(a,b,d,h,f,k,p)
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
  u=_D(a,b,d,h,f,k,u)
  u=_p(a,b,d,h,f,k,u,passes=2)
  u=_I(a,b,d,h,f,k,u)
  u=_p(a,b,d,h,f,k,u,passes=2)
  v=l(u)
  if v>s:
   s,t=(v,u)
 return[j[w]for w in t]
def _G(a,b,c,d,e,f,g):
 h=_F(a,b,c,d,e,f,g)
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
 n=_z(a,b,c,min(d,60),e,f,g,width=96)
 o=[(p*width+q)*4+r for p,q,r in n]
 o=_p(a,b,d,e+g,f,k,o)
 o=_I(a,b,d,e+g,f,k,o)
 o=_p(a,b,d,e+g,f,k,o,passes=2)
 n=[k[p][1]for p in o]
 return n if l(n)>m else h
class _H:
 def __init__(a,b,c,d,e,f,g,h):
  a.G=g[:]
  a.b=f
  a.z=0
  a.K=_o(b,c,d,e,f,h)
  i=d[:]
  for j in g:
   if j>=0:
    _l(i,b*b,f[j][0])
  a.F=sum((k==l for k,l in zip(i,e)))
  for j in reversed(g[2:]):
   if j>=0:
    a.K.e(j,wishes=True)
 def u(a,b):
  if b>a.z:
   c=range(a.z,b)
  else:
   c=range(a.z-1,b-1,-1)
  for d in c:
   e,f=(a.G[d],a.G[d+2])
   if e>=0:
    a.K.e(e)
   if f>=0:
    a.K.e(f,wishes=True)
  a.z=b
 def C(a,b,c):
  d=a.K
  e,f=a.G[a.z:a.z+2]
  g=_s(d,e)
  if e>=0:
   d.e(e)
  g+=_s(d,f)
  if e>=0:
   d.e(e)
  h=_s(d,b)
  if b>=0:
   d.e(b,wishes=bool(c))
  i,j=d.f()
  if b>=0:
   d.e(b,wishes=bool(c))
  k=(i,b)if c else(b,i)
  return(k,h+j-g)
 def a(a,b,c):
  a.G[a.z:a.z+2]=b
  a.F+=c
def _I(a,b,c,d,e,f,g,h=None):
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
 n=_H(a,b,d,e,f,g,m)
 if n.F==i:
  return[F for F in g if F>=0]
 if h is None:
  h=min(4000,max(300,900000//(a*a)))
 o,p=(n.F,n.G[:])
 q=max(1,h//4)
 r=l.randrange(c-1)
 n.u(r)
 s=1
 t=a-b+1
 for u in range(h):
  if u and u%q==0:
   l.shuffle(m)
   n=_H(a,b,d,e,f,p,m)
   r=l.randrange(c-1)
   n.u(r)
  v=u%2
  w=n.G[r+v]
  x=l.randrange(5)
  if x<2 and w>=0:
   y,z,A=f[w][1]
   y=min(t-1,max(0,y+l.choice((-2,-1,0,0,1,2))))
   z=min(t-1,max(0,z+l.choice((-2,-1,0,0,1,2))))
   B=(y*t+z)*4+l.randrange(4)
  elif x==4:
   B=-1
  else:
   B=l.randrange(len(f))
  C,D=n.C(B,v)
  E=0.4*(1-u%q/q)**2+0.04
  if D>=0 or l.random()<math.exp(D/E):
   n.a(C,D)
   if n.F>=o:
    o,p=(n.F,n.G[:])
    if o==i:
     break
  if l.randrange(16)==0:
   s=-s
  if not 0<=r+s<c-1:
   s=-s
  r+=s
  n.u(r)
 return[F for F in p if F>=0]
def _J(a,b,c,d,e,f,g):
 h=_G(a,b,c,d,e[:],f,g[:])
 if d<=2 or a<=16:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 l=a-b+1
 m=[(n*l+o)*4+p for n,o,p in h]
 m=_I(a,b,d,e+g,f,k,m)
 m=_p(a,b,d,e+g,f,k,m,passes=2)
 return[k[n][1]for n in m]
def _K():
 a=list(map(int,sys.stdin.buffer.read().split()))
 b,c,d,e=a[:4]
 f=b*b
 g=_J(b,c,d,e,a[4:4+f],a[4+f:4+2*f],a[4+2*f:])
 print(len(g))
 for h in g:
  print(*h)
if __name__=='__main__':
 _K()
