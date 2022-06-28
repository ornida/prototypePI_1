from model import Model

model = Model(2)

for agent in model.schedule.agent_buffer(shuffled=False):
    print("Retailer "+str(agent.unique_id+1)+"\ndemand: "+str(agent.demand)+"  lot size: "+str(agent.lot_size())+"\nlead time: "+ str(agent.leadtime)+"reorder: "+str(agent.reorderPoint))
print("-----------------------")
for i in range(10):
    model.step()
