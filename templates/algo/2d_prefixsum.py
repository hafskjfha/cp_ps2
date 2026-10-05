class prefixsum_2d:
    def __init__(self,W,H,a):
        self.ps = [[0] * (W + 1) for _ in range(H + 1)]
        for y in range(H):
            row = 0
            for x in range(W):
                row += a[y][x]
                self.ps[y + 1][x + 1] = self.ps[y][x + 1] + row
                
    def rect(self, y1, x1, y2, x2):
        return (self.ps[y2 + 1][x2 + 1]
                - self.ps[y1][x2 + 1]
                - self.ps[y2 + 1][x1]
                + self.ps[y1][x1])
