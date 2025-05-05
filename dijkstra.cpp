#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <climits>
#include <fstream>
using namespace std;
struct Edge{int to;unsigned weight;};
class Vertex{
public:
    string name;vector<Edge> adj;unsigned dist;int prev;bool visited;
    Vertex(const string& n):name(n),dist(UINT_MAX),prev(-1),visited(false){}
};
struct Compare{bool operator()(Vertex* a,Vertex* b)const{return a->dist>b->dist;}};
int main(){
    ifstream file("graph_input.txt");
    if(!file){cerr<<"Failed to open graph_input.txt\n";return 1;}
    int N,M;file>>N>>M;
    vector<Vertex> V;V.reserve(N);string u,v;
    for(int i=0;i<N;++i){file>>u;V.emplace_back(u);}
    unordered_map<string,int> idx;
    for(int i=0;i<N;++i)idx[V[i].name]=i;
    for(int i=0;i<M;++i){
        unsigned w;file>>u>>v>>w;
        int iu=idx[u],iv=idx[v];
        V[iu].adj.push_back({iv,w});V[iv].adj.push_back({iu,w});
    }
    file>>u;int s=idx[u];V[s].dist=0;
    priority_queue<Vertex*,vector<Vertex*>,Compare> pq;pq.push(&V[s]);
    while(!pq.empty()){
        Vertex* wv=pq.top();pq.pop();
        if(wv->visited)continue;
        wv->visited=true;
        for(auto& e:wv->adj){
            Vertex* x=&V[e.to];
            if(x->visited)continue;
            unsigned alt=wv->dist+e.weight;
            if(alt<x->dist){x->dist=alt;x->prev=idx[wv->name];pq.push(x);}
        }
    }
    for(auto& vert:V){
        cout<<"Path to "<<vert.name<<" (cost "<<vert.dist<<"): ";
        vector<string> path;
        for(int i=idx[vert.name];i!=-1;i=V[i].prev)path.push_back(V[i].name);
        reverse(path.begin(),path.end());
        for(auto& nm:path)cout<<nm<<" ";
        cout<<'\n';
    }
    return 0;
}