import sys
input=sys.stdin.readline

from random import randint

class set(set):
    _global_seed = randint(1 << 59, 1 << 60)

    def __init__(self, iterable=None):
        self.seed = self.__class__._global_seed
        super().__init__()
        if iterable:
            self.update(iterable)
    
    def __iter__(self):
        for e in super().__iter__():
            yield e ^ self.seed

    def __contains__(self, key):
        return super().__contains__(key ^ self.seed)

    def add(self, key):
        super().add(key ^ self.seed)
    
    def update(self, iterable):
        for e in iterable:
            self.add(e)
    
    def remove(self, key):
        super().remove(key ^ self.seed)
    
    def discard(self, key):
        super().discard(key ^ self.seed)
    
    def copy(self):
        new = self.__class__()
        for e in self:
            new.add(e)
        return new
    
    def pop(self):
        return super().pop() ^ self.seed
    
    def clear(self):
        super().clear()

    def __or__(self, other):
        result = self.__class__()
        result.update(self)
        result.update(other)
        return result

    def __ror__(self, other):
        return self.__class__(other) | self

    def __ior__(self, other):
        self.update(other)
        return self

    def __and__(self, other):
        result = self.__class__()
        for e in self:
            if e in other:
                result.add(e)
        return result

    def __rand__(self, other):
        result = self.__class__()
        for e in other:
            if e in self:
                result.add(e)
        return result

    def __iand__(self, other):
        kept = [e for e in self if e in other]
        self.clear()
        self.update(kept)
        return self

    def __sub__(self, other):
        result = self.__class__()
        for e in self:
            if e not in other:
                result.add(e)
        return result

    def __rsub__(self, other):
        result = self.__class__()
        for e in other:
            if e not in self:
                result.add(e)
        return result

    def __isub__(self, other):
        for e in list(self):
            if e in other:
                self.discard(e)
        return self

    def __xor__(self, other):
        result = self.__class__()
        for e in self:
            if e not in other:
                result.add(e)
        for e in other:
            if e not in self:
                result.add(e)
        return result

    def __rxor__(self, other):
        return self.__xor__(other)

    def __ixor__(self, other):
        new = [e for e in self if e not in other]
        for e in other:
            if e not in self:
                new.append(e)
        self.clear()
        self.update(new)
        return self


def solve():
    n=int(input())
    a=[*map(int,input().split())]
    
    s=set()
    for i in range(n):
        s.add(a[i]-(i+1))
    
    arr=sorted(list(s))
    ans=1
    temp=1
    for i in range(1,len(arr)):
        if arr[i]-1==arr[i-1]:
            temp+=1
        else:
            ans=max(temp,ans)
            temp=1
    
    print(max(ans,temp))

def main():
    t=int(input())
    for _ in range(t):
        solve()
main()