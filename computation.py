"""
Holds the Computation class.
"""
from itertools import combinations
import networkx as nx
import pandas as pd
pd.options.display.max_rows = 1000
class Computation:
    """
    Handles the Computation part of the application. Returns profitable links when given crypto
    market data.
    """
    def __init__(self,crypto_data=0):
        """
        Initializes the Computation class using a dictionary containing crypto market data.
        Format of dictionary: {Ticker: Price}
        """
        print("Computation Constructor")
        if crypto_data == 0:
            self.test = {"eth":{"bch":10.606162,"eth":1.0,"btc":0.05763696,"ltc":21.081658,
            "eos":1206},"eos":{"bch":0.00879502,"eth":0.00082927,"btc":4.779e-05,
            "ltc":0.01748169,"eos":1.0},"ltc":{"bch":0.50298168,"eth":0.04742545,
            "btc":0.00273335,"ltc":1.0,"eos":57.186},"btc":{"bch":184.088,"eth":17.357382,
            "btc":1.0,"ltc":365.908,"eos":20930},"bch":{"bch":1.0,"eth":0.09429245,
            "btc":0.00543429,"ltc":1.98768,"eos":113.681}}
        else:
            self.test = crypto_data
        #self.age = age Sets to global variable
        self.graph = nx.DiGraph()

    def generate_graph(self):
        """
        Generates a graph from the data, with the weights being conversion rates.
        """
        print("Computation Generate Graph")
        for node1 in self.test.keys():
            for node2 in  self.test.keys():
                if self.test[node1]!= self.test[node2][node1]:
                    self.graph.add_edge(node1,node2,weight = self.test[node1][node2])

    def scan_graph(self):
        """
        Finds a path that generates the most profit.
        """
        arb_checks = []
        for comb1, comb2 in combinations(self.graph.nodes, 2):
            for path in nx.all_simple_paths(self.graph, comb1,
            comb2): #generates path from two points
                path_weight1 = 1 #intial evaluation
                for i in range(len(path) - 1):
                    path_weight1 *= self.graph[path[i]][path[i+1]]['weight'] #find profibility
                path.reverse()
                path_weight2 = 1

                for i in range(len(path) - 1):
                    path_weight2 *= self.graph[path[i]][path[i+1]]['weight']
                factor = path_weight1 * path_weight2 #checks profitability
                arb_checks.append((path, factor))#Add Link with Profitibility

        arb_checks = pd.DataFrame(arb_checks, columns=['Path', 'Result'])
        arb_checks = arb_checks[arb_checks['Result'] > 1.0]
        arb_checks =arb_checks.sort_values(by='Result', ascending=False)
        return arb_checks

#obj = Computation()
#obj.generate_graph()
#obj.scan_graph()
