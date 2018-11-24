// Includes
// ========
// STL includes
#include <iostream>
#include <bits/stdc++.h>
#include <cstdlib>
// BGL includes
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/cycle_canceling.hpp>
#include <boost/graph/push_relabel_max_flow.hpp>
#include <boost/graph/successive_shortest_path_nonnegative_weights.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/graph/find_flow_cost.hpp>

// BGL Graph definitions
// ===================== 
// Graph Type with nested interior edge properties for Cost Flow Algorithms
typedef boost::adjacency_list_traits<boost::vecS, boost::vecS, boost::directedS> Traits;
typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::directedS, boost::no_property,
    boost::property<boost::edge_capacity_t, long,
        boost::property<boost::edge_residual_capacity_t, long,
            boost::property<boost::edge_reverse_t, Traits::edge_descriptor,
                boost::property <boost::edge_weight_t, long> > > > > Graph; // new!
// Interior Property Maps
typedef boost::property_map<Graph, boost::edge_capacity_t>::type      EdgeCapacityMap;
typedef boost::property_map<Graph, boost::edge_weight_t >::type       EdgeWeightMap; // new!
typedef boost::property_map<Graph, boost::edge_residual_capacity_t>::type ResidualCapacityMap;
typedef boost::property_map<Graph, boost::edge_reverse_t>::type       ReverseEdgeMap;
typedef boost::graph_traits<Graph>::vertex_descriptor          Vertex;
typedef boost::graph_traits<Graph>::edge_descriptor            Edge;
typedef boost::graph_traits<Graph>::out_edge_iterator  OutEdgeIt; // Iterator

typedef unsigned int uint;

// Custom Edge Adder Class, that holds the references
// to the graph, capacity map, weight map and reverse edge map
// ===============================================================
class EdgeAdder {
    Graph &G;
    EdgeCapacityMap &capacitymap;
    EdgeWeightMap &weightmap;
    ReverseEdgeMap  &revedgemap;

public:
    EdgeAdder(Graph &G, EdgeCapacityMap &capacitymap, EdgeWeightMap &weightmap, ReverseEdgeMap &revedgemap) 
        : G(G), capacitymap(capacitymap), weightmap(weightmap), revedgemap(revedgemap) {}

    void addEdge(int u, int v, long c, long w) {
        Edge e, rev_e;
        boost::tie(e, boost::tuples::ignore) = boost::add_edge(u, v, G);
        boost::tie(rev_e, boost::tuples::ignore) = boost::add_edge(v, u, G);
        capacitymap[e] = c;
        weightmap[e] = w; // new!
        capacitymap[rev_e] = 0;
        weightmap[rev_e] = -w; // new
        revedgemap[e] = rev_e; 
        revedgemap[rev_e] = e; 
    }
};

#define USER(idx) (idx)
#define STATION(idx) (idx+N)
#define IDX_STATION(idx) (idx-N)

void solve_flow(){
	int N, M; std::cin >> N >> M;
	assert(N>0 && M>0);
    // Create Graph and Maps
    Graph G(N+M);
    EdgeCapacityMap capacitymap = boost::get(boost::edge_capacity, G);
    EdgeWeightMap weightmap = boost::get(boost::edge_weight, G);
    ReverseEdgeMap revedgemap = boost::get(boost::edge_reverse, G);
    ResidualCapacityMap rescapacitymap = boost::get(boost::edge_residual_capacity, G);
    EdgeAdder eaG(G, capacitymap, weightmap, revedgemap);

	Vertex source = boost::add_vertex(G);
	Vertex sink = boost::add_vertex(G);

	// Add the edges btw the source and the users
	// All have capicity one and cost 0
	for(int i=0; i<N; i++){
		eaG.addEdge(source, USER(i), 1, 0);
	}
    
    // Add the edges btw users and stations
	// All of capacity one and read the cost from matrix.
	// Negative cost = unspecified route -> no edge
	for(int i=0; i<N; i++){
		for(int j=0; j<M; j++){
			int cost_i_j; std::cin >> cost_i_j;
			if(cost_i_j >= 0)
				eaG.addEdge(USER(i), STATION(j), 1, cost_i_j);		
		}
	}

	// Add edges btw the stations and the sink
	// They have zero cost (for now) and capacity equal 
	// to the number of remaining spots in the station	
	for(int i=0; i<M; i++){
		int capacity; std::cin >> capacity;
		if(capacity > 0)
			eaG.addEdge(STATION(i), sink, capacity, 0);
	}

    // Option 2: Min Cost Max Flow with successive_shortest_path_nonnegative_weights
    boost::successive_shortest_path_nonnegative_weights(G, source, sink);
    int cost2 = boost::find_flow_cost(G);
    int s_flow = 0;
    // Iterate over all edges leaving the source to sum up the flow values.
    OutEdgeIt e, eend;
    for(boost::tie(e, eend) = boost::out_edges(boost::vertex(source,G), G); e != eend; ++e) {
        s_flow += capacitymap[*e] - rescapacitymap[*e];
    }
	if(s_flow < N){
		std::cerr << "[NOTE] Not all users could be mapped to a station\n";
	}

	// Iterate over the outedges from the users and find their mapping.
	for(int i=0; i<N; i++){	
		Vertex v_user = USER(i);
		for(boost::tie(e, eend) = boost::out_edges(boost::vertex(v_user,G), G); e != eend; ++e) {
			int f = capacitymap[*e] - rescapacitymap[*e];
			// if it is a match, output the matching
			if(f > 0){
				std::cout << IDX_STATION(boost::target(*e, G)) << "\n";	
			}
		}
	}
}

int main() {
	solve_flow();
    return 0;
}
