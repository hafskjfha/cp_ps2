import random
import subprocess
import sys
import math


temp=dict()

def generate():
    n = random.randint(1, 7)
    l = random.randint(1,100)
    a = [random.randint(1, 1) for _ in range(n)]

    s=""
    #s += "1\n"
    s += f"{n} {l}\n"
    s += " ".join(map(str, a)) + "\n"

    return s

def check(out1,out2):
    return out1==out2



for tc in range(1, 100000):
    inp = generate()

    my = subprocess.run(
        ["python", sys.argv[1]],
        input=inp,
        text=True,
        capture_output=True,
        timeout=2
    )

    brute = subprocess.run(
        ["python", sys.argv[2]],
        input=inp,
        text=True,
        capture_output=True,
        timeout=2
    )

    out1 = my.stdout.strip()
    out2 = brute.stdout.strip()

    if check(out1,out2)==False:
        print("WA FOUND!")
        print("Test:", tc)

        print("\nINPUT:")
        print(inp)

        print("MY OUTPUT:")
        print(out1)

        print("BRUTE OUTPUT:")
        print(out2)
        break

    if tc % 100 == 0:
        print(tc, "tests passed")