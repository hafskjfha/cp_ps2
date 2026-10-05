m,s=open(0).read().split()
if m=='S':
    if s=='R':print('S')
    else:print('M')
elif m=='R':
    if s=='P':print('S')
    else:print('M')
elif m=='P':
    if s=='S':print('S')
    else:print('M')
else:print('S')