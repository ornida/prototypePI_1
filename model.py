from random import shuffle
import mesa
import numpy as np
import math
from mesa.time import RandomActivation


class RetailAgent(mesa.Agent):
    """An agent with a fixed inventory"""
    def __init__(self, unique_id, model, demand, holdCost, orderCost, reorderPoint, leadtime, inv):
        super().__init__(unique_id, model)
        self.demand = demand
        self.holdCost = holdCost
        self.orderCost = orderCost
        self.reorderPoint = reorderPoint
        self.leadtime = leadtime
        self.inv_net = inv
        self.inv_pos =inv
        self.incoming_order = []

    def lot_size(self):
        #Economical Order Quantity 
        lotSize = math.ceil(math.sqrt(2*self.orderCost*self.demand/self.holdCost))
        return lotSize

    def safety_stock(self):
        ss = self.reorderPoint-self.demand
        return ss
    

    def order(self):
        self.inv_pos += self.lot_size()
        self.incoming_order.append(self.model.time + self.leadtime)
        self.incoming_order.sort()
             # if time == lt:
             # inv_net += self.lot_size
        #think about how to add leadtime into order
    
    def step(self):
        self.inv_net -= self.demand
        self.inv_pos -= self.demand
        while(len(self.incoming_order) > 0 and self.incoming_order[0]==self.model.time):
            self.incoming_order.pop()
            self.inv_net += self.lot_size
        if self.inv_pos <= self.reorderPoint:
            self.order()
        print("Retailer "+str(self.unique_id+1)+"\nnet inventory: "+str(self.inv_net)+"  inventory position: "+str(self.inv_pos))



class Model(mesa.Model):
    """A model with some numbers of agents"""
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.time = 0
        #create agents
        for i in range(self.num_agents):
            d = round(np.random.normal(10, 2))
            h = np.random.random_integers(5, 15)
            A = np.random.random_integers(10, 15)
            r = np.random.random_integers(3, 6)
            lt = np.random.random_integers(2, 8)
            inv = np.random.random_integers(20, 30)
            a = RetailAgent(i, self, d, h, A, r, lt, inv)
            self.schedule.add(a)
    
    def step(self):
        """Advance the model by one step"""
        self.schedule.step()

