#include <bits/stdc++.h>
using namespace std;

struct Edge { int to; unsigned weight; };

class Vertex {
public:
    string name;               // Vertex name
    vector<Edge> adj;          // adjacent vertices
    unsigned dist;             // distance estimate D(v)
    int prev;                  // previous vertex index
    bool visited;              // in N'
    Vertex(const string& n) : name(n), dist(UINT_MAX), prev(-1), visited(false) {}
};

struct Compare {
    bool operator()(Vertex* a, Vertex* b) const {
        return a->dist > b->dist;
    }
};

int main() {
    int N, M;
    cin >> N >> M;             // #vertices, #edges
    vector<Vertex> V;          // all vertices
    V.reserve(N);
    string u, v;

    // Read vertex names
    for (int i = 0; i < N; ++i) {
        cin >> u;
        V.emplace_back(u);
    }
    unordered_map<string,int> idx;
    for (int i = 0; i < N; ++i) idx[V[i].name] = i;

    // Read edges
    for (int i = 0; i < M; ++i) {
        unsigned w;
        cin >> u >> v >> w;
        int iu = idx[u], iv = idx[v];
        V[iu].adj.push_back({iv, w});
        V[iv].adj.push_back({iu, w});  // undirected
    }

    // Read source and initialize
    cin >> u;
    int s = idx[u];
    // 1. Initialization:
    //    N' = {u}
    //    for all v:
    //      if v adjacent to u: D(v) = c(u,v)
    //      else D(v) = ∞
    V[s].dist = 0;
    priority_queue<Vertex*, vector<Vertex*>, Compare> pq;
    pq.push(&V[s]);

    // 2. Loop until all vertices processed
    while (!pq.empty()) {
        Vertex* wv = pq.top(); pq.pop();
        if (wv->visited) continue;
        wv->visited = true;     // add w to N'
        // update neighbors
        for (auto& e : wv->adj) {
            Vertex* x = &V[e.to];
            if (x->visited) continue;
            unsigned alt = wv->dist + e.weight;
            // D(x) = min(D(x), D(w)+c(w,x))
            if (alt < x->dist) {
                x->dist = alt;
                x->prev = idx[wv->name];
                pq.push(x);
            }
        }
    }

    // Output shortest paths
    for (auto& vert : V) {
        cout << "Path to " << vert.name << " (cost " << vert.dist << "): ";
        vector<string> path;
        for (int i = idx[vert.name]; i != -1; i = V[i].prev)
            path.push_back(V[i].name);
        reverse(path.begin(), path.end());
        for (auto& nm : path) cout << nm << " ";
        cout << '\n';
    }
    return 0;
} 