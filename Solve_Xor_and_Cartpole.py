
## Hunar Ahmad @ Brainxyz.com

import random;
import math;
from matplotlib import pylab as plt

################ helper functions #####################
def gen_weight(): 
  return random.uniform(-1,1);

def activationF(val):
    return math.tanh(val)
#  return max(0, val)

############### MODEL ##########################
class Edge:
    # defines two weighted connections between 2 nodes
    def __init__(self):
        self.fW = gen_weight(); #father weight
        self.cW = self.fW; #child weight
        self._from = None; #from source Node
        self.to = None; #to target Node
    
    # mutate the child weight    
    def mutateEdge(self, lr):
        self.cW = self.fW + ( gen_weight()* lr)
    
    # replaces the father weight (fW) with child weight (cW)
    def childBecomesFather(self):
        self.fW = self.cW;
        
class Node:
    # defines node structure with their connections (Edges)
    def __init__(self):
        self.fY =0; #initial father activity
        self.cY =0; #initial child activity
        self.from_edges =[];
        self.to_edges=[];
        
    def spreadOut(self):
        # spreading the activation to the connected nodes
        for e in self.to_edges:
            e.to.fY += self.fY * e.fW;
            e.to.cY += self.cY * e.cW;
    
    # defines the connection                    
    def connectTo(self, net, targNode, weight):
        edge = Edge();
        edge.fW = weight;
        edge.cW = weight;
        edge._from = self;
        edge.to = targNode;
        
        net.edgeList.append(edge); # stores all the edges into a list
        
        self.to_edges.append(edge);
        targNode.from_edges.append(edge);

class Layer:
    # defines the layer
    def __init__(self):
        self.nodes = [];
        
    def appendNodes(self, num):
        for i in range(num):
            self.nodes.append(Node())
            
    def resetLayer(self):
        for n in self.nodes:
            n.fY =0;
            n.cY =0;

    def spreadOut(self):
        for n in self.nodes:
            n.spreadOut()
            
    def activate(self):
        for n in self.nodes:
            n.fY = activationF(n.fY);
            n.cY = activationF(n.cY);
        
    ## fully connected layers        
    def fconnectTo(self, net, targLayer):
        for sn in self.nodes:
            for tn in targLayer.nodes:
                sn.connectTo(net, tn, gen_weight());
    
    ## sparsely connected layers, randomly connected            
    def sconnectTo(self, net, targLayer, sparse_rate):
        for sn in self.nodes:
            for tn in targLayer.nodes:
                if(random.random() < sparse_rate):
                    sn.connectTo(net, tn, gen_weight());
                
################# NETWORK STRUCTURE ############################        
class Network:
    # defines the network
    def __init__(self, L1, L2, L3):        
        self.edgeList =[];
        self.sensor = Layer();
        self.hidden = Layer();
        self.out = Layer();
        
        self.sensor.appendNodes(L1);
        self.hidden.appendNodes(L2);
        self.out.appendNodes(L3);
        
    def fullyConnect(self):
        ## fully connected
        self.sensor.fconnectTo(self, self.hidden);
        self.hidden.fconnectTo(self, self.out);
        
    def sparseConnect(self, amount):
        ## sparsely connected
        self.sensor.sconnectTo(self, self.hidden, amount[0]);
        self.hidden.sconnectTo(self, self.out, amount[1]);
                
    def setInput(self, inputs):
        for i in range(len(inputs)):
            self.sensor.nodes[i].fY = inputs[i];
            self.sensor.nodes[i].cY = inputs[i];
            
    def forward(self, inputs):        
        self.setInput(inputs);          
        self.sensor.spreadOut();
        self.hidden.activate();
        self.hidden.spreadOut();
                          
    def mutateWeights(self, lr):
        for e in self.edgeList:
            e.mutateEdge(lr);
            
    def updateWeights(self):
        for e in self.edgeList:
            e.childBecomesFather();             
            
    def resetNet(self):
        self.sensor.resetLayer();
        self.hidden.resetLayer();
        self.out.resetLayer();               

################## USER AREA ########################

Problem = "cartpole"  ## Problem types: cartpole, xor

##### 1. XOR #######
if(Problem == "xor"):
    print("XOR Problem")
    
    epochs = 1000;
    lr = 0.1; #mutation rate similar to learning rate
    
    ## network configuration: input=2, hidden_nodes = 5, output =1
    net = Network(2, 5, 1); 
    net.fullyConnect();
    #net.sparseConnect([0.5, 1]);
    
    # data & labels: XOR problem
    inputs=[[0,0],[1,1],[0,1],[1,0]];
    labels=[0,0,1,1];
    
    # training loop 
    print("Training Started ...")
    ers =[];
    for i in range(epochs):
        fE=0; cE=0; # initialize father Erorr (fE) and child Error (cE)
        for j in range(len(labels)):     
            net.resetNet();
            net.forward(inputs[j]);        
            # calculates the network error 
            fE = fE + abs(net.out.nodes[0].fY - labels[j]);
            cE = cE + abs(net.out.nodes[0].cY - labels[j]);
        
        # update if the child performs better than the father i.e. the child network becomes the father of the next gneration  
        if(fE > cE):
            net.updateWeights()
        
        ## mutate again
        net.mutateWeights(lr)
            
        if(i % 10 ==0):
            ers.append(fE);
    print("Training Finished")
    ## asses the trained network
    print("Network Assesment - XOR problem")
    for j in range(len(labels)):
        net.resetNet();
        inp = inputs[j];
        label = labels[j];
        net.forward(inp);
        print( "target:",label ," pred:", net.out.nodes[0].fY )
            
    plt.plot(ers)
    plt.title("Error")

#### 2. Cartpole Problem #####
elif(Problem == "cartpole"):
    print("Cartpole Problem") 
       
    import gym
     
    lr = 0.1 ## mutation rate (similar to learning rate)
    epi = 100 ## number of episodes
    step_limit = 200
    
    ## configure the network structure
    n_input=4
    n_nodes=10
    n_output=1
    net = Network(n_input, n_nodes, n_output); 
    net.fullyConnect();
    #net.sparseConnect([0.5, 1]);

    env = gym.make("CartPole-v0")

    print("Training Started...")
    observation = env.reset()
    step_progress=[];    
    for i in range(epi):
        
        net.mutateWeights(lr) ## makes a mutated child copy from the father copy
        stepsF = [];
        stepsC = []

        ### evaluates the father network
        observation =  env.reset() 
        action = 0
        for step in range(step_limit):                 
            net.resetNet()
            net.forward(observation)    
            output = net.out.nodes[0].fY ##output of father network            
            action = 1 if output > 0 else 0
            observation, reward, done, info = env.step(action)            
            if(done==True):
                stepFather = step
                break
            
        ### evaluates the mutated child network
        observation =  env.reset() 
        action = 0
        for step in range(step_limit):                 
            net.resetNet()
            net.forward(observation)    
            output = net.out.nodes[0].cY ##output of child network          
            action = 1 if output > 0 else 0
            observation, reward, done, info = env.step(action)            
            if(done==True):
                stepChild = step
                break
              
        if(stepChild > stepFather):
            net.updateWeights()
            
        step_progress.append(stepChild)            
    env.close()
    print("Training Finished")
    
    plt.figure(1)
    plt.plot(step_progress)
    plt.title("Performance")
    
    # #### render the trained network
    # observation = env.reset()
    # action = 0
    # for t in range(500):
    #     env.render()
    #     net.resetNet()
    #     net.forward(observation)    
    #     output = net.out.nodes[0].cY            
    #     action = 1 if output > 0 else 0
    #     observation, reward, done, info = env.step(action)
    #     if(done==True):
    #         steps = t
    #         break
    # print("step:", steps)
    # env.close()


            


