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
   t.add(tuple(q.M))
   v,w=q.g()
   if v<0 or(v==0 and(not _b or p==0)):
    break
   x=-1
   while w:
    y=w&-w
    z=q.C[y.bit_length()-1]
    if v>0 or tuple((q.s[A]for A in q.b[z][0]))not in t:
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
  a.z,a.m,a.i=(b,c,d)
  a.s,a.P,a.M=(e,f,g)
  a.x=sum((C==D for C,D in zip(e,f)))
  a.v=_c(e+g,f)
  key=(b,c,d,tuple(f))
  i=_g._geometry_cache
  if i is not None and i[0]==key:
   a.I,a.b,a.w,a.k=i[1:]
  else:
   a.I=[]
   a.b=[]
   a.w=[]
   a.k=[[]for _ in e]
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
     u=len(a.I)
     a.I.append(t)
     for o in t:
      a.k[o].append(u)
     for k in range(4):
      t=tuple((s+C for C in j[k]))
      a.b.append((t,(q,r,k)))
      a.w.append(sum((1<<d*C+f[D]for C,D in enumerate(t))))
   _g._geometry_cache=(key,a.I,a.b,a.w,a.k)
  a.C=list(range(len(a.b)))if h is None else h
  a.j=[sum((e[D]==f[D]for D in C))for C in a.I]
  a.N=sum((1<<d*C+D for C,D in enumerate(g)))
  a.L=c*c
  a.c=(1<<len(a.b))-1
  a.Q=[[0]*d for _ in g]
  a.H=[0]*len(a.I)
  for v,w in enumerate(a.C):
   x=1<<v
   a.H[w>>2]|=x
   for y,o in enumerate(a.b[w][0]):
    a.Q[y][f[o]]|=x
  a.B=[0]*4
  for u,z in enumerate(a.j):
   A=a.L-z
   for B in range(4):
    if A&1<<B:
     a.B[B]|=a.H[u]
 def q(a,b):
  return(a.N&a.w[b]).bit_count()-a.j[b>>2]
 def e(a,b):
  c,_=a.b[b]
  d,e,f=(a.s,a.M,a.P)
  g={}
  for h,i in enumerate(c):
   j,k=(d[i],e[h])
   e[h],d[i]=(j,k)
   l=(k==f[i])-(j==f[i])
   a.x+=l
   if l:
    for m in a.k[i]:
     g[m]=g.get(m,0)+l
  n,o,p=(a.j,a.B,a.H)
  q=a.L
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
  u=a.i
  a.N=sum((1<<u*v+w for v,w in enumerate(e)))
 def g(a):
  b=[0]*5
  for c,d in enumerate(a.M):
   e=a.Q[c][d]
   f=0
   while e:
    g=b[f]
    b[f]=g^e
    e&=g
    f+=1
  e=0
  for f in range(4):
   h,i=(b[f],a.B[f])
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
  return(l-a.L,k)
 def f(a):
  b,c=a.g()
  d=(c&-c).bit_length()-1
  return(b,a.C[d])
 def p(a,b,width=64):
  c,d=(a.N,a.j)
  e=[(c&D).bit_count()-d[C>>2]for C,D in enumerate(a.w)]
  f=[C for C,D in enumerate(e)if D>=-2]
  b.shuffle(f)
  g=sorted(f,key=lambda C:e[C],reverse=True)[:8]
  h=g+f
  i,j=(set(),set())
  k,l=(0,None)
  m=0
  n=a.j[:]
  o=a.B[:]
  p=a.x
  for q in h:
   if q in j:
    continue
   j.add(q)
   r,_=a.b[q]
   s=tuple((a.s[C]for C in r))
   t=(s,e[q])
   if t in i:
    continue
   i.add(t)
   u=e[q]
   a.e(q)
   v,w=a.f()
   x=u+v
   y,z=(a.s,a.M)
   for A,B in enumerate(r):
    z[A],y[B]=(y[B],z[A])
   a.j[:]=n
   a.B[:]=o
   a.x=p
   a.N=c
   if x>k:
    k,l=(x,(q,w))
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
  while len(p)<d and o.x<o.v:
   q,r=o.f()
   if q>0:
    o.e(r)
    p.append(o.b[r][1])
   elif len(p)+2<=d:
    s=o.p(m)
    if s is None:
     break
    for r in s:
     o.e(r)
     p.append(o.b[r][1])
   else:
    break
  t=sum((u==v for u,v in zip(o.s,f)))
  if t>j:
   j,k=(t,p)
  if j==o.v:
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
 def p(a,b,width=64,min_gain=-2):
  c,d=(a.N,a.j)
  e=[(c&D).bit_count()-d[C>>2]for C,D in enumerate(a.w)]
  f=[C for C,D in enumerate(e)if D>=min_gain]
  b.shuffle(f)
  g=sorted(f,key=lambda C:e[C],reverse=True)[:8]
  h=g+f
  i,j=(set(),set())
  k,l=(0,None)
  m=0
  n=a.j[:]
  o=a.B[:]
  p=a.x
  for q in h:
   if q in j:
    continue
   j.add(q)
   r,_=a.b[q]
   s=tuple((a.s[C]for C in r))
   t=(s,e[q])
   if t in i:
    continue
   i.add(t)
   u=e[q]
   a.e(q)
   v,w=a.f()
   x=u+v
   y,z=(a.s,a.M)
   for A,B in enumerate(r):
    z[A],y[B]=(y[B],z[A])
   a.j[:]=n
   a.B[:]=o
   a.x=p
   a.N=c
   if x>k:
    k,l=(x,(q,w))
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
 while len(l)<d and h.x<h.v:
  m,n=h.f()
  if m>0:
   if len(l)+2<=d:
    o=h.p(k,width=8,min_gain=max(1,m-1))
    if o is not None:
     n=o[0]
   h.e(n)
   l.append(h.b[n][1])
  elif len(l)+2<=d:
   o=h.p(k)
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
_p={}
class _q:
 def __init__(a,b,c,d,e,f,g):
  h,i=(b*b,c*c)
  a.A,a.n=(h,i)
  a.s,a.M=(d[:h],d[h:])
  a.U,a.V=(e[:],[6]*i)
  a.b,a.C=(f,g)
  j=len(f)
  a.d=(1<<j)-1
  key=(b,c)
  k=_o.get(key)
  if k is None:
   l=[[0]*h for _ in range(i)]
   m=[15<<4*E for E in range(j//4)]
   n=[f[E][0]for E in range(0,j,4)]
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
  a.E,a.H,a.I,a.k=k
  v=_p.get(key)
  if v is None:
   v=[sum((a.H[F]for F in E))for E in a.k]
   _p[key]=v
  a.l=v
  a.values=[[0]*7 for _ in range(i)]
  a.r=[[0]*7 for _ in range(i)]
  for u in range(i):
   w,x=(a.values[u],a.r[u])
   for r,y in enumerate(a.E[u]):
    w[a.s[r]]|=y
    x[a.U[r]]|=y
  a.R=[0]*j.bit_length()
  for z,s in enumerate(g):
   t=1<<s
   while z:
    A=z&-z
    a.R[A.bit_length()-1]|=t
    z^=A
  a.j=[sum((a.s[F]==a.U[F]for F in E))for E in a.I]
  a.B=[0]*5
  for p,B in enumerate(a.j):
   C=i-B
   for D in range(4):
    if C&1<<D:
     a.B[D]|=a.H[p]
  a.j=None
 def e(a,b,wishes=False):
  if wishes:
   c,d,e,f=(a.U,a.V,a.r,a.s)
  else:
   c,d,e,f=(a.s,a.M,a.values,a.U)
  g=a.E
  h,i=(a.B,a.l)
  for j,k in enumerate(a.b[b][0]):
   l,m=(c[k],d[j])
   if l!=m:
    for n in range(a.n):
     o=g[n][k]
     e[n][l]^=o
     e[n][m]^=o
    p=(m==f[k])-(l==f[k])
    if p:
     q=i[k]
     r=0
     if p>0:
      while q:
       s=h[r]
       h[r]=s^q
       q&=~s
       r+=1
     else:
      while q:
       s=h[r]
       h[r]=s^q
       q&=s
       r+=1
    d[j],c[k]=(l,m)
 def f(a):
  b=[0]*5
  for c in range(a.n):
   for d in(a.values[c][a.V[c]],a.r[c][a.M[c]]):
    e=0
    while d:
     f=b[e]
     b[e]=f^d
     d&=f
     e+=1
  d=0
  for e in range(5):
   g,h=(b[e],a.B[e])
   i=g^h
   b[e]=i^d
   d=g&h|i&d
  j,k=(a.d,0)
  for e in range(4,-1,-1):
   l=j&b[e]
   if l:
    j=l
    k|=1<<e
  m=k-a.n-sum((p==q for p,q in zip(a.M,a.V)))
  if m<0:
   return(-1,0)
  for n in reversed(a.R):
   if not j&j-1:
    break
   o=j&~n
   if o:
    j=o
  return((j&-j).bit_length()-1,m)
def _r(a,b,c,d,e,f,g,passes=8,offset=0,seed_offset=0):
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
  q=_q(a,b,n,e,f,p)
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
class _s:
 def __init__(a,b,c,d,e,f):
  a.A=f
  a.b=d
  a.K=e[:]
  a.F=[b[:]]
  for g in e:
   h=a.F[-1][:]
   if g>=0:
    _l(h,f,d[g][0])
   a.F.append(h)
  a.U=[None]*(len(e)+1)
  a.U[-1]=c+[-1]*(len(b)-f)
  for i in range(len(e)-1,-1,-1):
   j=a.U[i+1][:]
   if e[i]>=0:
    _l(j,f,d[e[i]][0])
   a.U[i]=j
  a.J=sum((k==l for k,l in zip(a.F[-1],c)))
 def o(a,b,c):
  d,e=(a.A,a.b)
  f=a.F[b][:]
  g=set(range(d,len(f)))
  for h,i in zip(a.K[b:b+len(c)],c):
   if h>=0:
    g.update(e[h][0])
   if i>=0:
    j=e[i][0]
    g.update(j)
    _l(f,d,j)
  k=a.F[b+len(c)]
  wishes=a.U[b+len(c)]
  return sum(((f[l]==wishes[l])-(k[l]==wishes[l])for l in g))
 def a(a,b,c,d):
  e,f=(a.A,a.b)
  a.K[b:b+len(c)]=c
  for g in range(b,len(a.K)):
   h=a.F[g][:]
   i=a.K[g]
   if i>=0:
    _l(h,e,f[i][0])
   a.F[g+1]=h
  for g in range(b+len(c)-1,-1,-1):
   j=a.U[g+1][:]
   i=a.K[g]
   if i>=0:
    _l(j,e,f[i][0])
   a.U[g]=j
  a.J+=d
def _t(a,b,c,d,e,f,g,h=None):
 if c<2:
  return g
 i,j=(a*a,b*b)
 k=_s(d,e,f,g+[-1]*(c-len(g)),i)
 if k.J==_c(d,e):
  return g
 l=random.Random(sum(((B+7)*C for B,C in enumerate(d)))+c*977+9167)
 width=a-b+1
 if h is None:
  h=min(2400,max(160,450000//i))
 for m in range(h):
  n=l.randrange(c-1)
  o=m%2
  p=k.K[n+o]
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
   v=k.F[n][:]
   if u>=0:
    _l(v,i,f[u][0])
   w,_=_m(v,k.U[n+2],f,i,j,current=k.K[n+1],allow_zero=True)
   x=[u,w]
  else:
   y=k.U[n+2][:]
   if u>=0:
    _l(y,i,f[u][0])
   z,_=_m(k.F[n],y,f,i,j,current=k.K[n],allow_zero=True)
   x=[z,u]
  if k.K[n:n+2]==x:
   continue
  A=k.o(n,x)
  if A>0 or(A==0 and l.randrange(8)==0):
   k.a(n,x,A)
   if k.J==_c(d,e):
    break
 return[B for B in k.K if B>=0]
def _u(a,b):
 if b<0:
  return 0
 c=0
 for d,e in enumerate(a.b[b][0]):
  f,g=(a.M[d],a.s[e])
  h,i=(a.U[e],a.V[d])
  c+=(f==h)+(g==i)-(g==h)-(f==i)
 return c
def _v(a,b,wishes=False):
 if b<0:
  return None
 if wishes:
  c,d,e=(a.U,a.V,a.r)
 else:
  c,d,e=(a.s,a.M,a.values)
 f=a.b[b][0]
 g=(wishes,f,[c[h]for h in f],d[:],[h[:]for h in e],a.j[:]if a.j is not None else None,a.B[:])
 a.e(b,wishes=wishes)
 return g
def _w(a,b):
 if b is None:
  return
 wishes,c,d,e,f,g,h=b
 i=a.U if wishes else a.s
 for j,k in zip(c,d):
  i[j]=k
 if wishes:
  a.V,a.r=(e,f)
 else:
  a.M,a.values=(e,f)
 a.j,a.B=(g,h)
def _x(a,b,c,d):
 e=_u(a,b)
 f=_v(a,b)
 e+=_u(a,c)
 _w(a,f)
 g=(b,c)
 if e<0:
  e,g=(0,(-1,-1))
 for h,i in d:
  j=_u(a,h)
  f=_v(a,h,wishes=bool(i))
  k,l=a.f()
  _w(a,f)
  m=j+l
  if m>=e:
   e=m
   g=(k,h)if i else(h,k)
 return g
def _y(a,b,c,d,e,f,g,passes=4,width=32):
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
  o=_q(a,b,l,e,f,n)
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
   s,t=_x(o,s,t,u)
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
def _z(a,b,c,d,e,f,g):
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
  p=_r(a,b,c,d,e,f,p,passes=4,seed_offset=37307*(o+1))
  x=i(p)
  if x>=j:
   m,j=(p,x)
   if x==k:
    break
 return m
class _A(_g):
 def __init__(a,b,c,d,e,f,g,h=None):
  super().__init__(b,c,d,e,f,g,h)
  a.T=[2 if min(r//b,r%b,b-1-r//b,b-1-r%b)<c-1 else 1 for r in range(b*b)]
  a.L=2*c*c
  a.t=[[0]*d for _ in g]
  for i,j in enumerate(a.C):
   k=1<<i
   for l,m in enumerate(a.b[j][0]):
    if a.T[m]==2:
     a.t[l][f[m]]|=k
  a.j=[sum((a.T[s]for s in r if e[s]==f[s]))for r in a.I]
  a.B=[0]*6
  for n,o in enumerate(a.j):
   p=a.L-o
   for q in range(6):
    if p&1<<q:
     a.B[q]|=a.H[n]
 def q(a,b):
  return sum((a.T[d]for c,d in enumerate(a.b[b][0])if a.M[c]==a.P[d]))-a.j[b>>2]
 def e(a,b):
  c,_=a.b[b]
  d,e,f=(a.s,a.M,a.P)
  g={}
  for h,i in enumerate(c):
   j,k=(d[i],e[h])
   e[h],d[i]=(j,k)
   l=(k==f[i])-(j==f[i])
   a.x+=l
   if l:
    l*=a.T[i]
    for m in a.k[i]:
     g[m]=g.get(m,0)+l
  n,o,p=(a.j,a.B,a.H)
  q=a.L
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
  u=a.i
  a.N=sum((1<<u*v+w for v,w in enumerate(e)))
 def g(a):
  b=[0]*6
  for c,d in enumerate(a.M):
   e=a.t[c][d]
   for f,g in((0,a.Q[c][d]^e),(1,e)):
    while g:
     h=b[f]
     b[f]=h^g
     g&=h
     f+=1
  g=0
  for f in range(6):
   i,j=(b[f],a.B[f])
   k=i^j
   b[f]=k^g
   g=i&j|k&g
  l,m=(a.c,0)
  for f in range(5,-1,-1):
   n=l&b[f]
   if n:
    l=n
    m|=1<<f
  return(m-a.L,l)
def _B(a,b,c,d,e,f,g):
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
  q=_A(a,b,c,e[:],f,g[:],k[:])
  r,s,t=([],set(),l)
  for _ in range(d):
   s.add(tuple(q.M))
   u,v=q.g()
   if u<0:
    break
   w=-1
   while v:
    x=v&-v
    y=q.C[x.bit_length()-1]
    if u>0 or tuple((q.s[z]for z in q.b[y][0]))not in s:
     w=y
     break
    v^=x
   if w<0:
    break
   if u>0:
    s.clear()
   t+=sum(((q.M[z]==f[A])-(q.s[A]==f[A])for z,A in enumerate(q.b[w][0])))
   q.e(w)
   r.append(q.b[w][1])
   if t>m:
    m,n=(t,r[:])
   if m==o:
    return n
 return n
def _C(a,b,c,d,e,f,g):
 h=_c(e+g,f)
 i=sum((y==z for y,z in zip(e,f)))
 if i==h:
  return[(h,[])]
 j,k,l,m,n=_d(a,b,f)
 width=a-b+1
 o=[]
 for p in(_f,_h,_k,_B):
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
def _D(a,b,c,d,e,f,g):
 h=_C(a,b,c,d,e[:],f,g[:])
 if h[0][0]==_c(e+g,f):
  return h[0][1]
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 width=a-b+1
 l=e+g
 m,n=(-1,[])
 for _,o in h[:4]:
  p=[(t*width+u)*4+v for t,u,v in o]
  p=_r(a,b,d,l,f,k,p,passes=2)
  q=l[:]
  for r in p:
   _l(q,a*a,k[r][0])
  s=sum((t==u for t,u in zip(q,f)))
  if s>m:
   m,n=(s,p)
 p=_r(a,b,d,l,f,k,n,passes=6,offset=2)
 p=_y(a,b,d,l,f,k,p)
 p=_t(a,b,d,l,f,k,p)
 p=_r(a,b,d,l,f,k,p,passes=2)
 p=_z(a,b,d,l,f,k,p)
 return[k[t][1]for t in p]
def _E(a):
 b=object.__new__(_g)
 b.__dict__=a.__dict__.copy()
 b.s=a.s[:]
 b.M=a.M[:]
 b.j=a.j[:]
 b.B=a.B[:]
 return b
def _F(a,b):
 c,d=(a.N,a.j)
 e=[(c&q).bit_count()-d[p>>2]for p,q in enumerate(a.w)]
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
   o=tuple((a.s[p]for p in a.b[h][0]))
   if n.get(o,0)>=2:
    continue
   n[o]=n.get(o,0)+1
   k.append((h,e[h]))
   m-=1
   if m==0:
    break
 return k
def _G(a,b,c,d,e,f,g,width=24):
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
   for z,A in _F(w,p):
    if y and z==y[-1]:
     continue
    B=_E(w)
    B.e(z)
    C=bytes(B.s)+bytes(B.M)
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
   key=tuple(w.M)
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
def _H(a,b,c,d,e,f,g):
 h=_g(a,b,c,e[:],f,g[:])
 i,j=h.f()
 k,l=(max(0,i),[j]if i>0 else[])
 if d==1:
  return[h.b[s][1]for s in l]
 m=[(h.q(s),s)for s in range(len(h.b))]
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
def _I(a,b,c,d,e,f,g):
 if d<=2:
  return _H(a,b,c,d,e,f,g)
 h=_D(a,b,c,d,e[:],f,g[:])
 if d>24:
  return h
 i=_G(a,b,c,d,e,f,g,width=24 if d<=12 else 12)
 j,_,k,_,_=_d(a,b,f)
 l=list(zip(j,k))
 width=a-b+1
 m=[(w*width+x)*4+y for w,x,y in i]
 m=_r(a,b,d,e+g,f,l,m)
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
def _J(a,b,c,d,e,f):
 g=_u(a,b)
 h=_v(a,b)
 g+=_u(a,c)
 i=_v(a,c)
 g+=_u(a,d)
 _w(a,i)
 _w(a,h)
 j=(b,c,d)
 for b in e:
  k=_u(a,b)
  h=_v(a,b)
  for d in f:
   l=_u(a,d)
   i=_v(a,d,wishes=True)
   c,m=a.f()
   _w(a,i)
   n=k+l+m
   if n>=g:
    g=n
    j=(b,c,d)
  _w(a,h)
 return j
def _K(a,b,c,d,e,f,g,passes=2):
 if c<3:
  return g
 h=a*a
 i=_c(d,e)
 j=a-b+1
 k=random.Random(sum(((H+17)*I for H,I in enumerate(d)))+c*1777+71983)
 for l in range(passes):
  g=g+[-1]*min(6,c-len(g))
  m=d[:]
  for n in g:
   if n>=0:
    _l(m,h,f[n][0])
  if sum((H==I for H,I in zip(m,e)))==i:
   return[H for H in g if H>=0]
  o=list(range(len(f)))
  k.shuffle(o)
  p=_q(a,b,m,e,f,o)
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
      if p.U[D]<6 and p.s[D]!=p.U[D]:
       break
     z=min(j-1,max(0,D//a-k.randrange(b)))
     A=min(j-1,max(0,D%a-k.randrange(b)))
     C=(z*j+A)*4+k.randrange(4)
    else:
     C=k.randrange(len(f))
    x.append(list(dict.fromkeys((r,-1,w,C))))
   for E in x[1]:
    F=_v(p,E,wishes=True)
    G,_=p.f()
    _w(p,F)
    if G not in x[0]:
     x[0].append(G)
   t,u,v=_J(p,t,u,v,*x)
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
  g=[H for H in g if H>=0]
 return g
def _L(a,b,c,d,e,f,g):
 h=_I(a,b,c,d,e[:],f,g[:])
 if d<=2:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 l=a-b+1
 m=[(n*l+o)*4+p for n,o,p in h]
 m=_K(a,b,d,e+g,f,k,m)
 m=_r(a,b,d,e+g,f,k,m,passes=2)
 return[k[n][1]for n in m]
def _M(a,b,c,d,e,f,g):
 if a>16 or d<=2:
  return _L(a,b,c,d,e,f,g)
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
 n=_r(a,b,d,h,f,k,n)
 n=_y(a,b,d,h,f,k,n)
 n=_t(a,b,d,h,f,k,n)
 n=_r(a,b,d,h,f,k,n,passes=2)
 o=_z(a,b,d,h,f,k,n)
 if d<=24:
  p=_G(a,b,c,d,e,f,g,width=24 if d<=12 else 12)
  p=[(w*width+x)*4+y for w,x,y in p]
  p=_r(a,b,d,h,f,k,p)
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
  u=_K(a,b,d,h,f,k,u)
  u=_r(a,b,d,h,f,k,u,passes=2)
  u=_P(a,b,d,h,f,k,u)
  u=_r(a,b,d,h,f,k,u,passes=2)
  v=l(u)
  if v>s:
   s,t=(v,u)
 return[j[w]for w in t]
def _N(a,b,c,d,e,f,g):
 h=_M(a,b,c,d,e,f,g)
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
 n=_G(a,b,c,min(d,60),e,f,g,width=96)
 o=[(p*width+q)*4+r for p,q,r in n]
 o=_r(a,b,d,e+g,f,k,o)
 o=_P(a,b,d,e+g,f,k,o)
 o=_r(a,b,d,e+g,f,k,o,passes=2)
 n=[k[p][1]for p in o]
 return n if l(n)>m else h
class _O:
 def __init__(a,b,c,d,e,f,g,h):
  a.K=g[:]
  a.b=f
  a.D=0
  a.O=_q(b,c,d,e,f,h)
  i=d[:]
  for j in g:
   if j>=0:
    _l(i,b*b,f[j][0])
  a.J=sum((k==l for k,l in zip(i,e)))
  for j in reversed(g[2:]):
   if j>=0:
    a.O.e(j,wishes=True)
  a.h=sum((k==l for k,l in zip(a.O.s+a.O.M,a.O.U+a.O.V)))
 def y(a,b):
  if b>a.D:
   c=range(a.D,b)
  else:
   c=range(a.D-1,b-1,-1)
  for d in c:
   e,f=(a.K[d],a.K[d+2])
   if e>=0:
    a.h+=_u(a.O,e)
    a.O.e(e)
   if f>=0:
    a.h+=_u(a.O,f)
    a.O.e(f,wishes=True)
  a.D=b
 def G(a,b,c):
  d=a.O
  e=a.J-a.h
  f=_u(d,b)
  g=_v(d,b,wishes=bool(c))
  h,i=d.f()
  _w(d,g)
  j=(h,b)if c else(b,h)
  return(j,f+i-e)
 def a(a,b,c):
  a.K[a.D:a.D+2]=b
  a.J+=c
def _P(a,b,c,d,e,f,g,h=None):
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
 n=_O(a,b,d,e,f,g,m)
 if n.J==i:
  return[F for F in g if F>=0]
 if h is None:
  h=min(4000,max(300,900000//(a*a)))
 o,p=(n.J,n.K[:])
 q=max(1,h//4)
 r=l.randrange(c-1)
 n.y(r)
 s=1
 t=a-b+1
 for u in range(h):
  if u and u%q==0:
   l.shuffle(m)
   n=_O(a,b,d,e,f,p,m)
   r=l.randrange(c-1)
   n.y(r)
  v=u%2
  w=n.K[r+v]
  x=l.randrange(5)
  if x==0 and w>=0:
   y,z,A=f[w][1]
   y=min(t-1,max(0,y+l.choice((-2,-1,0,0,1,2))))
   z=min(t-1,max(0,z+l.choice((-2,-1,0,0,1,2))))
   B=(y*t+z)*4+l.randrange(4)
  elif x==1:
   B=n.O.f()[0]
  elif x==4:
   B=-1
  else:
   B=l.randrange(len(f))
  C,D=n.G(B,v)
  E=0.4*(1-u%q/q)**2+0.04
  if D>=0 or l.random()<math.exp(D/E):
   n.a(C,D)
   if n.J>=o:
    o,p=(n.J,n.K[:])
    if o==i:
     break
  if l.randrange(16)==0:
   s=-s
  if not 0<=r+s<c-1:
   s=-s
  r+=s
  n.y(r)
 return[F for F in p if F>=0]
def _Q(a,b,c,d,e,f,g):
 h=_N(a,b,c,d,e[:],f,g[:])
 if d<=2 or a<=16:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 l=a-b+1
 m=[(n*l+o)*4+p for n,o,p in h]
 m=_P(a,b,d,e+g,f,k,m)
 m=_r(a,b,d,e+g,f,k,m,passes=2)
 return[k[n][1]for n in m]
def _R():
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
def _S(a,b,c,d):
 e=sum((u<<t for t,u in enumerate(a+c)))
 f=sum((u<<t for t,u in enumerate(b)))
 if e&65535==f:
  return[]
 g=e.bit_count()-f.bit_count()
 if not 0<=g<=9:
  return None
 h=_R()
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
def _T(a,b,c,d,e,f,g):
 if a==4 and b==3 and(c==2):
  h=_S(e,f,g,d)
  if h is not None:
   return[(i//8,i//4%2,i%4)for i in h]
 return _Q(a,b,c,d,e,f,g)
class _U:
 def __init__(a,b,c,d,e,f,g,h):
  i,j=(b*b,c*c)
  a.A,a.n=(i,j)
  a.s,a.M=(d[:i],d[i:])
  a.U,a.V=(e[:],[6]*j)
  a.T,a.W=(f[:],[0]*j)
  a.b,a.C=(g,h)
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
  a.E,a.H,a.I,a.k=k
  a.values=[[0]*7 for _ in range(j)]
  a.r=[[0]*7 for _ in range(j)]
  a.S=[[0]*3 for _ in range(j)]
  for u in range(j):
   v,w,x=(a.values[u],a.r[u],a.S[u])
   for r,y in enumerate(a.E[u]):
    v[a.s[r]]|=y
    w[a.U[r]]|=y
    x[a.T[r]]|=y
  a.R=[0]*len(g).bit_length()
  for z,s in enumerate(h):
   t=1<<s
   while z:
    A=z&-z
    a.R[A.bit_length()-1]|=t
    z^=A
  a.j=[sum((a.T[F]*(a.s[F]==a.U[F])for F in E))for E in a.I]
  a.B=[0]*6
  for p,B in enumerate(a.j):
   C=2*j-B
   for D in range(5):
    if C&1<<D:
     a.B[D]|=a.H[p]
 def e(a,b,wishes=False):
  c={}
  d,e,f=(a.E,a.k,a.j)
  if wishes:
   g,h=(a.U,a.V)
   i,j=(a.T,a.W)
   for k,l in enumerate(a.b[b][0]):
    m,n=(g[l],h[k])
    o,p=(i[l],j[k])
    if m!=n:
     for q in range(a.n):
      r=d[q][l]
      a.r[q][m]^=r
      a.r[q][n]^=r
    if o!=p:
     for q in range(a.n):
      r=d[q][l]
      a.S[q][o]^=r
      a.S[q][p]^=r
    s=a.s[l]
    t=p*(s==n)-o*(s==m)
    if t:
     for u in e[l]:
      c[u]=c.get(u,0)+t
    h[k],g[l]=(m,n)
    j[k],i[l]=(o,p)
  else:
   g,h=(a.s,a.M)
   for k,l in enumerate(a.b[b][0]):
    m,n=(g[l],h[k])
    if m==n:
     continue
    for q in range(a.n):
     r=d[q][l]
     a.values[q][m]^=r
     a.values[q][n]^=r
    t=a.T[l]*((n==a.U[l])-(m==a.U[l]))
    if t:
     for u in e[l]:
      c[u]=c.get(u,0)+t
    h[k],g[l]=(m,n)
  for u,t in c.items():
   if not t:
    continue
   v=f[u]
   f[u]+=t
   w=2*a.n-v^2*a.n-f[u]
   while w:
    x=w&-w
    a.B[x.bit_length()-1]^=a.H[u]
    w^=x
 def f(a):
  b=[0]*6
  for c in range(a.n):
   d=a.r[c][a.M[c]]
   e=[(d&a.S[c][1],0),(d&a.S[c][2],1)]
   f=a.W[c]
   if f:
    e.append((a.values[c][a.V[c]],f-1))
   for g,h in e:
    while g:
     i=b[h]
     b[h]=i^g
     g&=i
     h+=1
  g=0
  for h in range(6):
   j,k=(b[h],a.B[h])
   l=j^k
   b[h]=l^g
   g=j&k|l&g
  m,n=(a.d,0)
  for h in range(5,-1,-1):
   o=m&b[h]
   if o:
    m=o
    n|=1<<h
  p=sum((t*(u==v)for t,u,v in zip(a.W,a.M,a.V)))
  q=n-2*a.n-p
  if q<0:
   return(-1,0)
  for r in reversed(a.R):
   if not m&m-1:
    break
   s=m&~r
   if s:
    m=s
  return((m&-m).bit_length()-1,q)
def _V(a,b,c,d,e,f,g,h,passes=1):
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
  q=_U(a,b,n,e,f,g,p)
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
def _W(a,b,c,d,e,f,g):
 h=_T(a,b,c,d,e[:],f,g[:])
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
  F=_V(a,b,d,p,f,D,m,o)
  F=_r(a,b,d,p,f,m,F,passes=2)
  q=p[:]
  for r in F:
   _l(q,i,k[r])
  G=sum((H==I for H,I in zip(q,f)))
  if G>s:
   s,t=(G,F)
   if G==x:
    break
 return[l[H]for H in t]
class _X:
 def __init__(a,b,c,d,e,f,g,h):
  a.K=g[:]
  a.b=f
  a.D=0
  a.O=_q(b,c,d,e,f,h)
  i=d[:]
  for j in g:
   if j>=0:
    _l(i,b*b,f[j][0])
  a.J=sum((k==l for k,l in zip(i,e)))
  for j in reversed(g[3:]):
   if j>=0:
    a.O.e(j,wishes=True)
  a.h=sum((k==l for k,l in zip(a.O.s+a.O.M,a.O.U+a.O.V)))
 def y(a,b):
  if b>a.D:
   c=range(a.D,b)
  else:
   c=range(a.D-1,b-1,-1)
  for d in c:
   e,f=(a.K[d],a.K[d+3])
   if e>=0:
    a.h+=_u(a.O,e)
    a.O.e(e)
   if f>=0:
    a.h+=_u(a.O,f)
    a.O.e(f,wishes=True)
  a.D=b
 def u(a,b):
  c=a.O
  d=a.K[a.D if b else a.D+2]
  wishes=not bool(b)
  e=_v(c,d,wishes=wishes)
  f,_=c.f()
  _w(c,e)
  return f
 def G(a,b,c):
  d=a.O
  e=a.J-a.h
  f=_u(d,b)
  g=_v(d,b)
  f+=_u(d,c)
  h=_v(d,c,wishes=True)
  i,j=d.f()
  _w(d,h)
  _w(d,g)
  return((b,i,c),f+j-e)
 def a(a,b,c):
  a.K[a.D:a.D+3]=b
  a.J+=c
def _Y(a,b,c,d,e,f,g,h=None):
 import math
 if c<3:
  return g
 i=_c(d,e)
 j=d[:]
 for k in g:
  if k>=0:
   _l(j,a*a,f[k][0])
 if sum((H==I for H,I in zip(j,e)))==i:
  return[H for H in g if H>=0]
 l=random.Random(sum(((H+31)*I for H,I in enumerate(d)))+c*1123+19271)
 m=list(range(len(f)))
 l.shuffle(m)
 g=g+[-1]*(c-len(g))
 n=_X(a,b,d,e,f,g,m)
 if h is None:
  h=min(6000,max(600,1350000//(a*a)))
 o,p=(n.J,n.K[:])
 q=max(1,h//3)
 r=l.randrange(c-2)
 n.y(r)
 s=1
 t=a-b+1
 for u in range(h):
  if u and u%q==0:
   l.shuffle(m)
   n=_X(a,b,d,e,f,p,m)
   r=l.randrange(c-2)
   n.y(r)
  v,w=(n.K[r],n.K[r+2])
  x=u%2
  y=w if x else v
  z=l.randrange(5)
  if z==0 and y>=0:
   A,B,C=f[y][1]
   A=min(t-1,max(0,A+l.choice((-2,-1,0,0,1,2))))
   B=min(t-1,max(0,B+l.choice((-2,-1,0,0,1,2))))
   D=(A*t+B)*4+l.randrange(4)
  elif z==1:
   D=n.u(x)
  elif z==4:
   D=-1
  else:
   D=l.randrange(len(f))
  if x:
   w=D
  else:
   v=D
  E,F=n.G(v,w)
  G=0.4*(1-u%q/q)**2+0.04
  if F>=0 or l.random()<math.exp(F/G):
   n.a(E,F)
   if n.J>=o:
    o,p=(n.J,n.K[:])
    if o==i:
     break
  if c>3:
   if l.randrange(16)==0:
    s=-s
   if not 0<=r+s<c-2:
    s=-s
   r+=s
   n.y(r)
 return[H for H in p if H>=0]
def _Z(a,b,c,d,e,f,g):
 h=_W(a,b,c,d,e[:],f,g[:])
 if d<=2:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 l=a-b+1
 m=[(n*l+o)*4+p for n,o,p in h]
 m=_Y(a,b,d,e+g,f,k,m)
 m=_r(a,b,d,e+g,f,k,m,passes=2)
 return[k[n][1]for n in m]
def _aa():
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
_ab=None
_ac=None
def _ad(a,b):
 c=b|(1<<27)-1<<48
 d={c:b''}
 e=[c]
 for f in range(1,5):
  g=[]
  for h in e:
   i=d[h]
   for j,k in a(h):
    if k in d:
     continue
    l=i+bytes((j,))
    d[k]=l
    g.append(k)
    wishes=k
    m=bytearray()
    for n in range(25):
     o=wishes&7
     wishes>>=3
     if o!=7:
      m.append(n*6+o)
    yield(f,l,bytes(m))
  e=g
def _ae(a,b,c,d,e=8):
 global _ab,_ac
 if a==b:
  return[]
 if _c(a+c,b)<16:
  return None
 if _ab is None:
  _ab=_aa()
 f=_ab
 g=sum((N<<3*M for M,N in enumerate(a+c)))
 h=sum((N<<3*M for M,N in enumerate(b)))
 i=(1<<48)-1
 j={g:b''}
 k=[g]
 l=min(4,d,e)
 for _ in range(l):
  m=[]
  for n in k:
   o=j[n]
   for p,q in f(n):
    if q in j:
     continue
    r=o+bytes((p,))
    j[q]=r
    if q&i==h:
     return list(r)
    m.append(q)
  k=m
 s=min(4,d-l,e-l)
 if s<=0:
  return None
 t=list(j)
 u=(len(t)+7)//8
 v=[[bytearray(u)for _ in range(6)]for _ in range(25)]
 for w,n in enumerate(t):
  offset,x=(w>>3,1<<(w&7))
  for y in v:
   y[n&7][offset]|=x
   n>>=3
 z=[int.from_bytes(N,'little')for M in v for N in M]
 A=[M.bit_count()for M in z]
 B=A.__getitem__
 C=(1<<len(t))-1
 if _ac is None or _ac[0]!=h:
  _ac=[h,[],_ad(f,h)]
 D=_ac
 E=D[1]
 F=0
 while True:
  if F==len(E):
   if D[2]is None:
    break
   G=next(D[2],None)
   if G is None:
    D[2]=None
    break
   E.append(G)
  H,r,I=E[F]
  if H>s:
   break
  F+=1
  J=C
  for K in sorted(I,key=B):
   J&=z[K]
   if not J:
    break
  if J:
   L=t[(J&-J).bit_length()-1]
   return list(j[L]+r[::-1])
 return None
def _af(a,b,c,d,e,f,g):
 h=_Z(a,b,c,d,e,f,g)
 if a!=4 or b!=3 or len(h)>=d:
  return h
 i,_,j,_,_=_d(a,b,f)
 k,l=(e[:],g[:])
 for m,n,o in h:
  _e(k,l,i[(m*2+n)*4+o])
 p=_ae(k,f,l,d-len(h))
 return h+[j[q]for q in p]if p is not None else h
def _ag(a,b,c,d,e,f,g):
 h=_af(a,b,c,d,e,f,g)
 if a!=4 or b!=3 or d<6 or(_c(e+g,f)<16):
  return h
 i,_,j,_,_=_d(a,b,f)
 k,l=(e[:],g[:])
 for m,n,o in h:
  _e(k,l,i[(m*2+n)*4+o])
 if k==f:
  return h
 p=set()
 for q in(2,4,8,12):
  r=max(0,len(h)-q)
  if r in p:
   continue
  p.add(r)
  k,l=(e[:],g[:])
  for m,n,o in h[:r]:
   _e(k,l,i[(m*2+n)*4+o])
  s=_ae(k,f,l,d-r)
  if s is not None:
   return h[:r]+[j[t]for t in s]
 return h
def _ah(a,b,c,d,e,f,g):
 h=a*a
 wishes=d+[6]*(b*b)
 for i in reversed(f):
  if i>=0:
   _l(wishes,h,e[i][0])
 j=_q(a,b,c,wishes[:h],e,g)
 j.V=wishes[h:]
 k=f[:]
 for l,i in enumerate(f):
  if i>=0:
   j.e(i,wishes=True)
  m,_=j.f()
  k[l]=m
  if m>=0:
   j.e(m)
 return k
def _ai(a,b,c,d,e,f,g,passes=1,seed_offset=0):
 h=a*a
 i=_c(d,e)
 j=sum(((q+1)*r for q,r in enumerate(d)))+c*131+1000003+seed_offset
 k=random.Random(j)
 g=[q for q in g if q>=0]
 for l in range(passes):
  m=d[:]
  for n in g:
   _l(m,h,f[n][0])
  if sum((q==r for q,r in zip(m,e)))==i:
   return g
  o=g+[-1]*min(8,c-len(g))
  p=list(range(len(f)))
  k.shuffle(p)
  g=_ah(a,b,d,e,f,o,p)
  g=[q for q in g if q>=0]
 return g
def _aj(a,b,c,d,e,f,g):
 h=_ag(a,b,c,d,e[:],f,g[:])
 if d<=2:
  return h
 i=a*a
 j=e+g
 k,_,l,_,_=_d(a,b,f)
 m=list(zip(k,l))
 n=a-b+1
 o=[(w*n+x)*4+y for w,x,y in h]
 p=j[:]
 for q in o:
  _l(p,i,k[q])
 r=sum((w==x for w,x in zip(p,f)))
 s=_c(j,f)
 if r==s:
  return h
 t=o
 for u in range(2):
  o=_ai(a,b,d,j,f,m,o,seed_offset=u*104729)
  o=_r(a,b,d,j,f,m,o,passes=1,seed_offset=3301+u*7919)
  p=j[:]
  for q in o:
   _l(p,i,k[q])
  v=sum((w==x for w,x in zip(p,f)))
  if v>r:
   r,t=(v,o)
   if v==s:
    break
 return[l[w]for w in t]
def _ak(a):
 b=[]
 for c in range(4):
  d=[]
  for e in range(3):
   f=[]
   for g in range(512):
    h=0
    for i in range(3):
     j,k=((e,i),(i,2-e),(2-e,2-i),(2-i,e))[c]
     h|=(g>>3*i&7)<<3*(3*j+k)
    f.append(h)
   d.append(f)
  b.append(d)
 l=3*a*a
 m=(1<<l)-1
 n=3*a
 o=[]
 for j in range(a-2):
  for k in range(a-2):
   p=3*(a*j+k)
   q=m^(511|511<<n|511<<2*n)<<p
   o.append((p,q))
 def r(t,u):
  v=b[u]
  return v[0][t&511]|v[1][t>>9&511]|v[2][t>>18]
 def s(t):
  u,v=(t&m,t>>l)
  w=[r(v,F)for F in range(4)]
  x=[F&511|(F>>9&511)<<n|F>>18<<2*n for F in w]
  for y,(z,A)in enumerate(o):
   B=u>>z
   C=B&511|(B>>n&511)<<9|(B>>2*n&511)<<18
   D=u&A
   for E in range(4):
    yield(4*y+E,D|x[E]<<z|r(C,-E&3)<<l)
 return s
def _al(a,b,c,d,e):
 if e<=0:
  return None
 f=a*a
 g=sum((y==z for y,z in zip(b,c)))
 if g==_c(b+d,c):
  return None
 h=_ak(a)
 i=sum((z<<3*y for y,z in enumerate(b+d)))
 j=sum((z<<3*y for y,z in enumerate(c)))
 k=sum((1<<3*y for y in range(f)))
 l=random.Random(i+e*997)
 import heapq
 m=[(i,b'')]
 n={i}
 for o in range(min(6,e)):
  p={}
  for q,r in m:
   for s,t in h(q):
    if t in n or t in p:
     continue
    u=r+bytes((s,))
    v=t^j
    w=f-((v|v>>1|v>>2)&k).bit_count()
    if w>g:
     return list(u)
    p[t]=(w,l.getrandbits(32),u)
  if not p:
   break
  x=heapq.nlargest(256,p,key=p.get)
  m=[(y,p[y][2])for y in x]
  n.update(x)
 return None
def _am(a,b,c,d,e,f,g):
 h=_aj(a,b,c,d,e,f,g)
 if not 5<=a<=9 or b!=3 or len(h)>=d:
  return h
 i,_,j,_,_=_d(a,b,f)
 k,l=(e[:],g[:])
 width=a-b+1
 for m,n,o in h:
  _e(k,l,i[(m*width+n)*4+o])
 p=sum((t!=u for t,u in zip(k,f)))
 if not 1<=p<=8:
  return h
 q=h[:]
 for _ in range(4):
  r=_al(a,k,f,l,d-len(q))
  if r is None:
   break
  for s in r:
   _e(k,l,i[s])
   q.append(j[s])
 return q
def _an(a,b,c,d,e,f,g,h=None):
 import math
 if c<3:
  return g
 i=_c(d,e)
 j=d[:]
 for k in g:
  if k>=0:
   _l(j,a*a,f[k][0])
 if sum((H==I for H,I in zip(j,e)))==i:
  return[H for H in g if H>=0]
 l=random.Random(sum(((H+67)*I for H,I in enumerate(d)))+c*1559+925713)
 m=list(range(len(f)))
 l.shuffle(m)
 g=g+[-1]*(c-len(g))
 n=_X(a,b,d,e,f,g,m)
 if h is None:
  h=min(3000,max(300,675000//(a*a)))
 o,p=(n.J,n.K[:])
 q=max(1,h//3)
 r=l.randrange(c-2)
 n.y(r)
 s=1
 t=a-b+1
 for u in range(h):
  if u and u%q==0:
   l.shuffle(m)
   n=_X(a,b,d,e,f,p,m)
   r=l.randrange(c-2)
   n.y(r)
  v,w=(n.K[r],n.K[r+2])
  x=u%2
  y=w if x else v
  z=l.randrange(5)
  if z==0 and y>=0:
   A,B,C=f[y][1]
   A=min(t-1,max(0,A+l.choice((-2,-1,0,0,1,2))))
   B=min(t-1,max(0,B+l.choice((-2,-1,0,0,1,2))))
   D=(A*t+B)*4+l.randrange(4)
  elif z==1:
   D=n.u(x)
  elif z==4:
   D=-1
  else:
   D=l.randrange(len(f))
  if x:
   w=D
  else:
   v=D
  E,F=n.G(v,w)
  G=0.86*(1-u%q/q)**2+0.04
  if F>=0 or l.random()<math.exp(F/G):
   n.a(E,F)
   if n.J>=o:
    o,p=(n.J,n.K[:])
    if o==i:
     break
  if c>3:
   if l.randrange(16)==0:
    s=-s
   if not 0<=r+s<c-2:
    s=-s
   r+=s
   n.y(r)
 return[H for H in p if H>=0]
def _ao(a,b,c,d,e,f,g,h=None):
 if c<3:
  return g
 i=d[:]
 for j in g:
  if j>=0:
   _l(i,a*a,f[j][0])
 k=sum((m==n for m,n in zip(i,e)))
 if k==_c(d,e):
  return g
 l=_an(a,b,c,d,e,f,g,h)
 l=_r(a,b,c,d,e,f,l,passes=2)
 i=d[:]
 for j in l:
  if j>=0:
   _l(i,a*a,f[j][0])
 if sum((m==n for m,n in zip(i,e)))>k:
  return l
 return g
def _ap(a,b,c,d,e,f,g):
 h=_am(a,b,c,d,e[:],f,g[:])
 if d<3:
  return h
 i,_,j,_,_=_d(a,b,f)
 k=list(zip(i,j))
 width=a-b+1
 l=[(n*width+o)*4+p for n,o,p in h]
 m=_ao(a,b,d,e+g,f,k,l)
 if m==l:
  return h
 return[j[n]for n in m if n>=0]
def _aq(a,b,c,d,e,f):
 g=sum((a[j]==b[j]for j in f))
 for h in e:
  _e(a,c,d[h])
 i=sum((a[j]==b[j]for j in f))
 for h in reversed(e):
  _e(a,c,d[h])
 return i-g
def _ar(a,b,c,d,e,f,g,h=20000):
 if h<=0:
  return None
 width=a-b+1
 i=[J for J in range(a*a)if c[J]!=d[J]]
 if not i:
  return None
 j=a*a-len(i)
 k=_c(c+e,d)-j
 if k<=0:
  return None
 l=set()
 for m in i:
  n,o=divmod(m,a)
  for p in range(max(0,n-b+1),min(n,width-1)+1):
   for q in range(max(0,o-b+1),min(o,width-1)+1):
    r=(p*width+q)*4
    l.update(range(r,r+4))
 s=sorted(l)
 t=random.Random(g)
 t.shuffle(s)
 u=0
 v=None
 w=0
 x=set()
 y={}
 for z in s:
  p,q=divmod(z//4,width)
  A=[(J*width+K)*4+L for J in range(max(0,p-b+1),min(width,p+b))for K in range(max(0,q-b+1),min(width,q+b))for L in range(4)]
  t.shuffle(A)
  for B in A:
   if z==B:
    continue
   C=(min(z,B),max(z,B))
   if C in x:
    continue
   if w>=h:
    return v
   x.add(C)
   w+=1
   D=(min(z//4,B//4),max(z//4,B//4))
   E=y.get(D)
   if E is None:
    E=tuple(sorted(set(f[z])|set(f[B])))
    y[D]=E
   for F,G in((z,B),(B,z)):
    H=(F,G,F,G)
    I=_aq(c,d,e,f,H,E)
    if I>u:
     u,v=(I,H)
     if u==k:
      return v
 return v
def _as(a,b,c,d,e,f,g):
 h=_ap(a,b,c,d,e,f,g)
 if a>16 or d-len(h)<4:
  return h
 i,_,j,_,_=_d(a,b,f)
 width=a-b+1
 k,l=(e[:],g[:])
 for m,n,o in h:
  _e(k,l,i[(m*width+n)*4+o])
 p=sum((s==t for s,t in zip(k,f)))
 if not 1<=a*a-p<=12 or p>=_c(e+g,f):
  return h
 q=sum(((s+41)*t for s,t in enumerate(e+f+g)))+a*1009+b*9176+d*131
 r=_ar(a,b,k,f,l,i,q)
 if r is None:
  return h
 return h+[j[s]for s in r]
class _at:
 def __init__(a,b,c,d,e,f,g,h):
  a.K=g[:]
  a.b=f
  a.D=0
  i=b*b
  j=d[:]
  for k in g:
   if k>=0:
    _l(j,i,f[k][0])
  a.J=sum((l==m for l,m in zip(j,e)))
  wishes=e+[6]*(c*c)
  for k in reversed(g[4:]):
   if k>=0:
    _l(wishes,i,f[k][0])
  a.O=_q(b,c,d,wishes[:i],f,h)
  a.O.V=wishes[i:]
  a.h=sum((l==m for l,m in zip(d,wishes)))
 def y(a,b):
  if b>a.D:
   c=range(a.D,b)
  else:
   c=range(a.D-1,b-1,-1)
  for d in c:
   e,f=(a.K[d],a.K[d+4])
   if e>=0:
    a.h+=_u(a.O,e)
    a.O.e(e)
   if f>=0:
    a.h+=_u(a.O,f)
    a.O.e(f,wishes=True)
  a.D=b
 def G(a,b,c,d):
  e=a.O
  f=a.J-a.h
  g=_u(e,b)
  h=_v(e,b)
  g+=_u(e,c)
  i=_v(e,c,wishes=True)
  j,k=_x(e,a.K[a.D+1],a.K[a.D+2],d)
  g+=_u(e,j)
  l=_v(e,j)
  g+=_u(e,k)
  _w(e,l)
  _w(e,i)
  _w(e,h)
  return((b,j,k,c),g-f)
 def a(a,b,c):
  a.K[a.D:a.D+4]=b
  a.J+=c
def _au(a,b,c,d,e,f,g,h=None):
 import math
 if c<4:
  return g
 i=g+[-1]*min(8,c-len(g))
 j=random.Random(sum(((J+43)*K for J,K in enumerate(d)))+c*1733+74821)
 k=list(range(len(f)))
 j.shuffle(k)
 l=_at(a,b,d,e,f,i,k)
 m=_c(d,e)
 if l.J==m:
  return g
 if h is None:
  h=min(1800,max(120,180000//(a*a)))
 n,o=(l.J,l.K[:])
 p=a-b+1
 q=len(i)
 r=j.randrange(q-3)
 l.y(r)
 s=1
 for t in range(h):
  u,v=(l.K[r],l.K[r+3])
  w=t%2
  x=v if w else u
  y=j.randrange(5)
  if y==0 and x>=0:
   z,A,B=f[x][1]
   z=min(p-1,max(0,z+j.choice((-1,0,1))))
   A=min(p-1,max(0,A+j.choice((-1,0,1))))
   C=(z*p+A)*4+j.randrange(4)
  elif y==1:
   D=l.O
   E=j.randrange(a*a)
   for _ in range(10):
    E=j.randrange(a*a)
    if D.U[E]<6 and D.s[E]!=D.U[E]:
     break
   z=min(p-1,max(0,E//a-j.randrange(b)))
   A=min(p-1,max(0,E%a-j.randrange(b)))
   C=(z*p+A)*4+j.randrange(4)
  elif y==4:
   C=-1
  else:
   C=j.randrange(len(f))
  if w:
   v=C
  else:
   u=C
  if t%11==10:
   if w:
    u=j.randrange(len(f))
   else:
    v=j.randrange(len(f))
  F=[(l.K[r+1],0),(l.K[r+2],1),(-1,0),(-1,1),(j.randrange(len(f)),j.randrange(2))]
  G,H=l.G(u,v,F)
  I=0.04+0.76*(1-t/max(1,h-1))**2
  if H>=0 or j.random()<math.exp(H/I):
   l.a(G,H)
   if l.J>=n:
    n,o=(l.J,l.K[:])
    if n==m:
     break
  if q>4:
   if j.randrange(16)==0:
    s=-s
   if not 0<=r+s<q-3:
    s=-s
   r+=s
   l.y(r)
 return[J for J in o if J>=0]
def _av(a,b,c,d,e,f,g):
 h=_as(a,b,c,d,e[:],f,g[:])
 if d<4:
  return h
 i=a*a
 j=e+g
 k,_,l,_,_=_d(a,b,f)
 m=list(zip(k,l))
 width=a-b+1
 n=[(s*width+t)*4+u for s,t,u in h]
 o=j[:]
 for p in n:
  _l(o,i,k[p])
 q=sum((s==t for s,t in zip(o,f)))
 if q==_c(j,f):
  return h
 r=_au(a,b,d,j,f,m,n)
 if r==n:
  return h
 r=_r(a,b,d,j,f,m,r,passes=1,seed_offset=2947)
 o=j[:]
 for p in r:
  _l(o,i,k[p])
 if sum((s==t for s,t in zip(o,f)))<=q:
  return h
 return[l[s]for s in r]
def _aw(a,b,c,d,e):
 if e<=0:
  return None
 f=a*a
 g=sum((y==z for y,z in zip(b,c)))
 if g==_c(b+d,c):
  return None
 h=_ak(a)
 i=sum((z<<3*y for y,z in enumerate(b+d)))
 j=sum((z<<3*y for y,z in enumerate(c)))
 k=sum((1<<3*y for y in range(f)))
 l=random.Random(i+e*997)
 import heapq
 m=[(i,b'')]
 n={i}
 for o in range(min(8,e)):
  p={}
  for q,r in m:
   for s,t in h(q):
    if t in n or t in p:
     continue
    u=r+bytes((s,))
    v=t^j
    w=f-((v|v>>1|v>>2)&k).bit_count()
    if w>g:
     return list(u)
    p[t]=(w,l.getrandbits(32),u)
  if not p:
   break
  x=heapq.nlargest(512,p,key=p.get)
  m=[(y,p[y][2])for y in x]
  n.update(x)
 return None
def _ax(a,b,c,d,e,f,g):
 h=_av(a,b,c,d,e,f,g)
 if not 5<=a<=9 or b!=3 or d-len(h)<3:
  return h
 i,_,j,_,_=_d(a,b,f)
 k,l=(e[:],g[:])
 width=a-b+1
 for m,n,o in h:
  _e(k,l,i[(m*width+n)*4+o])
 p=sum((s!=t for s,t in zip(k,f)))
 if not 1<=p<=8:
  return h
 q=_aw(a,k,f,l,d-len(h))
 if q is None:
  return h
 for r in q:
  _e(k,l,i[r])
 if sum((s==t for s,t in zip(k,f)))<=a*a-p:
  return h
 return h+[j[s]for s in q]
def _ay():
 a=list(map(int,sys.stdin.buffer.read().split()))
 b,c,d,e=a[:4]
 f=b*b
 g=_ax(b,c,d,e,a[4:4+f],a[4+f:4+2*f],a[4+2*f:])
 print(len(g))
 for h in g:
  print(*h)
if __name__=='__main__':
 _ay()
