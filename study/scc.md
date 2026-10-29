# SCC (강한 연결 요소, Strongly Connected Component)

## 개요

SCC의 정의는
> SCC는 그 안의 모든 정점이 서로에게 도달할 수 있는 정점들의 최대 집합
이다.

주로 다음과 같은 문제에서 사용된다.
- 방향 그래프에서 서로 왕복 가능한 정점들을 그룹화
- 사이클이 존재하는 방향 그래프를 DAG로 압축
- SCC 압축 후 위상 정렬 / DP 적용
- 서로 도달 가능한 정점 집합을 구하는 문제

---
## 개념
방향 그래프에서 정점 집합 $S$가 있을 때,\
임의의 $u, v \in S$에 대해

$u$ → $v$로 가는 경로와\
$v$ → $u$로 가는 경로가

모두 존재한다면 $S$는 강하게 연결되어 있다고 한다.

이 조건을 만족하는 최대 정점 집합을 SCC라고 한다.

## 성질
그래프 $G$에서 모든 SCC를 하나 정점으로 압축하여 만든 그래프 $G'$는 DAG이다.

이점을 이용해 문제를 그래프로 모델링 후 SCC를 적절하게 처리하고 DAG로 변환하여 위상정렬+dp같은 기법등을 사용할 수 있다.

## 구현 - 코사라주(Kosaraju)
### 아이디어
> dfs 2번과 간선뒤집기 

1. 첫 번째 DFS에서 정점의 종료 순서를 기록합니다.
2. 모든 간선 방향을 뒤집은 역방향 그래프를 만듭니다.
3. 첫 번째 DFS에서 얻은 종료 순서의 역순, 즉 스택의 top부터 역방향 그래프에서 DFS를 돌립니다.
4. 이때 한 번의 DFS로 방문되는 정점들이 하나의 SCC입니다.

### 코드
```cpp
void dfs1(int cur) {
    visited[cur] = true;

    for (int next : graph[cur]) {
        if (!visited[next])
            dfs1(next);
    }

    // DFS 종료 시점에 저장
    order.push_back(cur);
}

void dfs2(int cur, vector<int>& scc) {
    visited[cur] = true;
    scc.push_back(cur);

    for (int next : revGraph[cur]) {
        if (!visited[next])
            dfs2(next, scc);
    }
}

int main(){
    // 1. 원래 그래프에서 DFS 종료 순서 구하기
    visited.assign(V + 1, false);

    for (int i = 1; i <= V; i++) {
        if (!visited[i])
            dfs1(i);
    }

    // 2. 역방향 그래프에서 종료 순서 역순으로 DFS
    visited.assign(V + 1, false);

    reverse(order.begin(), order.end());

    for (int node : order) {
        if (!visited[node]) {
            vector<int> scc;
            dfs2(node, scc);
            sccs.push_back(scc);
        }
    }
}
```

시간 복잡도 $O(V+E)$

## 구현 - 타잔(Tarjan)
### 아이디어
> DFS 1번

각 정점마다 두 값을 생각하는 것
```
id[u]  = u를 DFS에서 몇 번째로 방문했는가
low[u] = u의 DFS 서브트리에서
  아직 SCC가 확정되지 않은 정점들을 통해
  도달 가능한 가장 작은 id
```

DFS하면서 정점을 stack에 넣는다.

low[u]
= 현재 SCC 후보 안에서
  u가 거슬러 올라갈 수 있는
  가장 오래된 정점의 방문 번호

id[u] == low[u]\
→ u가 현재 SCC의 루트\
→ stack에서 u까지 pop

### 코드
```cpp
void dfs(int cur) {
    id[cur] = low[cur] = ++dfsCounter;
    st.push(cur);

    for (int next : graph[cur]) {
        // 아직 방문하지 않은 정점
        if (id[next] == 0) {
            dfs(next);
            low[cur] = min(low[cur], low[next]);
        }

        // 방문은 했지만 아직 SCC가 확정되지 않은 정점
        else if (!finished[next]) {
            low[cur] = min(low[cur], id[next]);
        }
    }

    // SCC의 루트
    if (id[cur] == low[cur]) {
        vector<int> scc;

        while (true) {
            int node = st.top();
            st.pop();

            finished[node] = true;
            scc.push_back(node);

            if (node == cur)
                break;
        }

        sccs.push_back(scc);
    }
}

int main(){
    for (int i = 1; i <= V; i++) {
        if (id[i] == 0)
            dfs(i);
    }
}
```

## 언제 떠올릴까?

방향 그래프에서 다음과 같은 표현이 나오면 SCC를 의심한다.

- 서로 왕복할 수 있는 정점들을 하나의 그룹으로 묶어야 할 때
- 사이클들을 하나의 정점처럼 취급하고 싶을 때
- 방향 그래프에 사이클이 있어서 바로 위상 정렬 / DAG DP를 사용할 수 없을 때
- 서로 도달 가능한 정점들이 같은 상태로 취급될 때
- SCC를 압축한 뒤 컴포넌트 사이의 관계를 처리해야 할 때

특히

> "SCC로 압축하면 DAG가 된다"

즉,

방향 그래프  
→ SCC 분리  
→ SCC를 하나의 정점으로 압축  
→ DAG  
→ 위상 정렬 / DP

의 흐름을 떠올린다.

## 핵심 한 줄

> SCC는 방향 그래프에서 서로 왕복 가능한 정점들을 최대 단위로 묶는 것이고, 모든 SCC를 압축하면 DAG가 된다.