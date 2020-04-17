import numpy as np

class Graph():
    def __init__(self , path , graph = dict() , circle = list()):
        self.data = np.loadtxt(path , delimiter= "," , dtype=np.int16)
        self.data = self.data[np.argsort(self.data[:,0])]
        self.graph = graph
        self.circlePath = circle
        self.tempPath = list()
        self.hasUsed = dict()
        self.stateKeys = list()
        self.stateValues = list()

    # 用dict表示图，dict的映射关系可以表示有向图的方向。

    def creatGraph(self):
        for i  in range(self.data.shape[0]):
            if self.graph.get(self.data[i , 0]) != None:
                self.graph[self.data[i , 0]].append(self.data[i , 1])
                self.graph[self.data[i , 0]].sort()
            else:
                self.graph[self.data[i , 0]] = [self.data[i , 1]]

    # 深度优先搜索算法，搜索图的环        
    def searchGraph(self):       
        for i in self.graph.keys():
            self.tempPath = [i]
            self.rootNode = i
            self.stateKeys = []
            self.stateValues = []
            self._searchRecursive(i)
            self.hasUsed[i] = True
            
        # print(self.circlePath)
        newList = []
        for i in range(3 , 8):
            for j in self.circlePath:
                if len(j) == i:
                    newList.append(j)
        # print("****"*20)
        # print(newList)
        # print(len(newList))
        with open("/projects/student/result.txt" , "w") as f:
            f.write(str(len(newList)) + "\n")
            for i in newList:
                for j in range(len(i)):
                    if j == len(i) - 1:
                        f.write(str(i[j])+"\n")
                    else:
                        f.write(str(i[j])+",")
    
    # 深度优先搜索，除了向前，全部情况都是后退。
    def _searchRecursive(self,fatherNode):
        fatherNodeLen = len(self.graph[fatherNode])
        for i in range(fatherNodeLen):
            nowNode = self.graph[fatherNode][i]
            # print(nowNode)
            if not self.hasUsed.get(nowNode) == True:               
                # self.tempPath.append(nowNode)
                # print("now path:",self.tempPath)
                # print(fatherNode in self.stateKeys)
                if fatherNode in self.stateKeys:
                    del self.stateValues[self.stateKeys.index(fatherNode)]               
                    
                    del self.stateKeys[self.stateKeys.index(fatherNode)]
                    
                if i < fatherNodeLen - 1:
                    self.stateKeys.append(fatherNode)
                    self.stateValues.append(1)
                else:
                    self.stateKeys.append(fatherNode)
                    self.stateValues.append(-1)
               
                # print("now visit node from {} to {}:".format(fatherNode ,nowNode))
                # print(self.stateKeys)
                # print(self.stateValues)
                if nowNode not in self.tempPath[1:-1]:
                    if nowNode == self.rootNode:
                        # print("\n****************************hava found a path*************************************:\n{}\n".format( self.tempPath) )
                        if 3 <= len(self.tempPath) <=7:
                            self.circlePath.append((self.tempPath.copy()))
                        # print(self.circlePath)
                        self._backNode()
                    elif not self.graph.get(nowNode) == None:
                        self.tempPath.append(nowNode)
                        # print("did not found path , now go deep")
                        self._searchRecursive(nowNode)
                    else:
                        self._backNode()
                        
                else:
                    self._backNode()
            else:
                self._backNode()

    # 节点回退到最近的一个未走完的节点。               
    def _backNode(self):       
        keys = self.stateKeys[::-1]
        values = self.stateValues[::-1]
        if 1 in values:
            del self.tempPath[self.tempPath.index(keys[values.index(1)])+1:]
            # print("back to:",self.tempPath[self.tempPath.index(keys[values.index(1)])])
            
                


if __name__ == "__main__":
    path = "/data/test_data.txt"
    graph = Graph(path)
    print(graph.data)
    graph.creatGraph()
    graph.searchGraph()
    