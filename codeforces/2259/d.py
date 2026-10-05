import sys

input=sys.stdin.readline

from random import randint

class dict(dict):
    _global_seed = randint(1<<59, 1<<60)

    def __init__(self, *args, **kwargs):
        self.seed = self.__class__._global_seed
        super().__init__()
        if args or kwargs:
            self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key ^ self.seed, value)

    def __getitem__(self, key):
        return super().__getitem__(key ^ self.seed)

    def __delitem__(self, key):
        super().__delitem__(key ^ self.seed)

    def __contains__(self, key):
        return super().__contains__(key ^ self.seed)

    def get(self, key, default=None):
        return super().get(key ^ self.seed, default)

    def pop(self, key, *args):
        return super().pop(key ^ self.seed, *args)

    def popitem(self):
        masked_key, value = super().popitem()
        return masked_key ^ self.seed, value

    def clear(self):
        super().clear()

    def update(self, *args, **kwargs):
        for mapping in args:
            if hasattr(mapping, 'items'):
                iterable = mapping.items()
            else:
                iterable = mapping
            for k, v in iterable:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def keys(self):
        for masked in super().keys():
            yield masked ^ self.seed

    def items(self):
        for masked, v in super().items():
            yield masked ^ self.seed, v

    def __iter__(self):
        return self.keys()

    def copy(self):
        new = self.__class__()
        for k, v in self.items():
            new[k] = v
        return new
    
    def __repr__(self):
        items = ', '.join(f'{k}: {v}' for k, v in self.items())
        return f'{self.__class__.__name__}({{{items}}})'
    
    def setdefault(self, key, default=None):
        return super().setdefault(key ^ self.seed, default)


def solve():
    n=int(input())
    a=[*map(int,input().split())]
    
    counter=dict()
    idx=dict()
    for i in range(n):
        idx.setdefault(a[i],[]).append(i)
        counter[a[i]]=counter.get(a[i],0)+1
    
    if counter.get(0,0)==1:
        print("NO")
        return
    
    keys=sorted(counter.keys())
    res=[None]*n
    flg=False
    
    for i in range(len(keys)):
        x=keys[i]
        idxs=idx[x]
        if flg:
            for j in idxs:
                res[j]="C"
        elif counter[x]>=3:
            res[idxs[0]]='A'
            res[idxs[1]]='B'
            res[idxs[2]]='C'
            for j in idxs[3:]:res[j]='A'
        else:
            for j,c in zip(idxs,"ABC"):
                res[j]=c
                flg=True
    
    #print(res)
    print("YES")
    print("".join(res))
    

def main():
    t=int(input())
    for _ in range(t):
        solve()
    
main()