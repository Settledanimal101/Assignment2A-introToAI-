import sys
from W4_Search import Problem, astar_search
from utils import distance

#读地图  
def load_problem(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    coords = {}
    graph = {}
    origin = None
    goals = []
    section = None

    for line in lines:
        if line.startswith("Nodes:"):
            section = "nodes"
        elif line.startswith("Edges:"):
            section = "edges"
        elif line.startswith("Origin:"):
            section = "origin"
        elif line.startswith("Destinations:"):
            section = "goals"
        elif section == "nodes" and ":" in line:
            node, pos = line.split(":")
            coords[int(node.strip())] = eval(pos.strip())
        elif section == "edges" and ":" in line:
            edge, cost = line.split(":")
            src, dst = eval(edge.strip())
            graph.setdefault(src, {})[dst] = int(cost.strip())
        elif section == "origin":
            origin = int(line.strip())
        elif section == "goals":
            goals = list(map(int, line.strip().split(";")))


    return coords, graph, origin, goals


class MyGraphProblem(Problem):    #自定义问题类来继承框架里的 Problem
    def __init__(self, initial, goals, graph, coords):
        super().__init__(initial)
        self.goals = goals
        self.graph = graph
        self.coords = coords

    def actions(self, state):
        return list(self.graph.get(state, {}).keys())

    def result(self, state, action):
        return action

    def goal_test(self, state):
        return state in self.goals

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + self.graph[A][B]

    def h(self, node):
        x1, y1 = self.coords[node.state]  
        return min(distance((x1, y1), self.coords[g]) for g in self.goals)   #用勾股定理32+42=52

# Step 3: 主程序（命令行入口）
if __name__ == "__main__":
   # if len(sys.argv) != 3:
  #      print("用法: python search.py <pathfinder> <AS>")        #NOT SURE ABOUT EXTANDE
      #  sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    coords, graph, origin, goals = load_problem(filename)

    if method == "AS":
        problem = MyGraphProblem(origin, goals, graph, coords)
        result = astar_search(problem)

        if result:
            path = [node.state for node in result.path()]
            #print(f"{filename} {method}")
            #print(f"{result.state} {len(result.path())}")
            print("the final path is :")
            print("  ".join(map(str, path)))
      #  else:              # 不确定针对此作业是否需要添加，对于无路径应该需要添加？但是只针对as十分不确定。。。。。
           # print("No path found.")
    # only support AS。。。。is it necessary to check if use other like gbfs /dfs...？。。。
