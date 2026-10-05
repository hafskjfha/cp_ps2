# Problem

You are given a colored $N \times N$ grid $A$, a $D \times D$ stamp $S$, and a target image $T$. Colors are represented by integers from 0 to $C-1$. Color 0 is treated in exactly the same way as every other color.

All coordinates are 0-indexed. The top-left cell is $(0,0)$. Row indices increase downward, and column indices increase to the right.

In one operation, perform the following:

* Choose the top-left coordinate $(x,y)$ of a $D \times D$ region and an integer $r \in {0,1,2,3}$.
* Rotate the stamp clockwise by $90r$ degrees from its reference orientation and place it on the selected region.
* Simultaneously swap the colors of all corresponding cells of the stamp and the grid that are in contact.
* Lift the stamp and return it to its reference orientation. The colors picked up from the grid remain on the stamp.

The stamp must not extend outside the grid. You may stamp the same region multiple times, and the selected region may overlap regions used in previous operations. Moving and rotating the stamp do not require additional operations. The rotation specified in each operation is always relative to the reference orientation and is not cumulative.

The position inside the selected region corresponding to stamp cell $(u,v)$ under rotation $r$ is defined as

$$
R_r(u,v)=
\begin{cases}
(u,v) & r=0,\\\\
(v,D-1-u) & r=1,\\\\
(D-1-u,D-1-v) & r=2,\\\\
(D-1-v,u) & r=3.
\end{cases}
$$

For every cell such that $R_r(u,v)=(p,q)$, swap $S_{u,v}$ and $A_{x+p,y+q}$.

Perform at most $K$ operations so that the number of cells in the final grid whose colors match the target $T$ is as large as possible. The target image never changes. Intermediate states and the final colors remaining on the stamp do not affect the score. You may also perform no operations at all. It is not guaranteed that all cells can be made to match.

## Score

If the number of matching cells in the final grid is $M$, the score for that input is

$$
P=\left\lfloor \frac{10^6 M}{N^2} \right\rfloor
$$

The total score is the sum of the scores over 40 evaluation inputs, with a maximum possible total score of $40,000,000$. Only an input on which your output is invalid or your program exceeds the execution limit receives a score of 0. The score does not depend on other contestants or on any reference solution. If multiple contestants have the same total score, they share the same rank.

## Input

Each input file contains one problem instance in the following format.

$$
N\ D\ C\ K
$$

$$
A\_{0,0}\ A\_{0,1}\ \cdots\ A\_{0,N-1}
$$

$$
\vdots
$$

$$
A\_{N-1,0}\ A\_{N-1,1}\ \cdots\ A\_{N-1,N-1}
$$

$$
T\_{0,0}\ T\_{0,1}\ \cdots\ T\_{0,N-1}
$$

$$
\vdots
$$

$$
T\_{N-1,0}\ T\_{N-1,1}\ \cdots\ T\_{N-1,N-1}
$$

$$
S\_{0,0}\ S\_{0,1}\ \cdots\ S\_{0,D-1}
$$

$$
\vdots
$$

$$
S\_{D-1,0}\ S\_{D-1,1}\ \cdots\ S\_{D-1,D-1}
$$

## Output

Output the number of operations $L$, followed by $x_i, y_i, r_i$ for each operation in order.

$$
L
$$

$$
x_0\ y_0\ r_0
$$

$$
\vdots
$$

$$
x\_{L-1}\ y\_{L-1}\ r\_{L-1}
$$

The following conditions must be satisfied.

* $0 \le L \le K$
* For every operation:

  * $0 \le x_i, y_i \le N-D$
  * $0 \le r_i \le 3$
* If $L=0$, output only `0`.
* Do not output any extra tokens.
* The output file size must not exceed 100,000 bytes.

## Constraints

* $3 \le N \le 30$
* $D \in {2,3}$, $D \le N$
* $2 \le C \le 6$
* $1 \le K \le 180$
* $0 \le A_{i,j}, T_{i,j} < C \quad (0 \le i,j < N)$
* $0 \le S_{u,v} < C \quad (0 \le u,v < D)$

## Limit
* time: 5s
* submit code size: 100,000B
* memory: 512mb