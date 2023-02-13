import random

#This function builds the network
def get_network(filename):
  f = open(filename, "r")
  network = []
  connection = ("", "")
  while connection[1] != "V":
    #Turns each router connection into tuples
    connection = tuple(f.readline()[:-1].split("|"))
    network.append(connection)
  f.close()
  return network

def build_network(network):
  graph = {}
  for connection in network:
    graph[connection[0]] = connection[1]
  return graph

#Parameters(The graph of the network, the amount of packets in the attack, the attackers input as a list, the users input as a list)
#Give most of the packets to the attackers and split it evenly, the users get a few packets, then split them into separate dictionaries
# def node_sampling(graph, num_packets, attackers, users, probability, rate):
#   #Sets up the packets marked dictionary with each router having its id as a key and the amount of packets marked in its name as its value
#   packets_marked = {}
#   for key in graph:
#     packets_marked[key] = 0

#   #Embeded function traverses through network sending packets
#   def mark_packets(senders, num_packets, probability):
#     #to_be_marked is the packet that is the last packet marked
#     to_be_marked = ""
#     num_packets //= len(senders)
#     current_packet = ""
#     for _ in range(num_packets):

#       #Sends packets to each of the 
#       for sender in senders:
#         current_packet = sender

#         #Traverses graph from user to victim
#         while "V" != current_packet:
#           if random.random() < probability:
#             to_be_marked = current_packet
#           current_packet = graph[current_packet]
#         if to_be_marked != "":
#           packets_marked[to_be_marked] += 1
#     return packets_marked

  

#   packets_marked = mark_packets(attackers, num_packets*rate, probability)
#   packets_marked = mark_packets(users, num_packets, probability)
#   return packets_marked

# def edge_sampling(graph, num_packets, attackers, users, probability, rate):
#   packets_marked = {}
#   for key in graph:
#     packets_marked[key + " | " + graph[key]] = 0

#   def mark_packets(senders, num_packets, probability):
    
#     to_be_marked = ""
#     num_packets //= len(senders)
#     current_packet = ""
#     for _ in range(num_packets):

#       #Sends packets to each of the 
#       for sender in senders:
#         previous_packet = sender
#         current_packet = graph[previous_packet]
#         edge = previous_packet+" | "+current_packet

#         #Traverses graph from user to victim
#         while "V" != current_packet:
#           if random.random() < probability:
#             to_be_marked = edge
#           previous_packet = current_packet
#           current_packet = graph[current_packet]
#           edge = previous_packet+" | "+current_packet
#         if to_be_marked != "":
#           packets_marked[to_be_marked] += 1
#     return packets_marked

#   packets_marked = mark_packets(attackers, num_packets*rate, probability)
#   packets_marked = mark_packets(users, num_packets, probability)
#   return packets_marked

def node_sampling(graph, attackers, users, probability, rate):
  #Sets up the packets marked dictionary with each router having its id as a key and the amount of packets marked in its name as its value
  packets_marked = {}
  for key in graph:
    packets_marked[key] = 0


  #to_be_marked is the packet that is the last packet marked
  to_be_marked = ""
  num_packets = 0
  current_packet = ""

  #gets number of users and attackers
  num_users = len(users)
  num_attackers = len(attackers)

  #Puts the attackers' routes in a list in order
  attackers_routes = []
  for _ in range(len(attackers)):
    attackers_routes.append([])
  current_index = 0
  for attacker in attackers:
    key = attacker
    while "V" != key:
      attackers_routes[current_index].append(key)
      key = graph[key]
    current_index+=1

  #Gets all the user nodes
  user_nodes = []
  all_attackers =  [attacker for sublist in attackers_routes for attacker in sublist]
  for key in graph:
    if key not in all_attackers:
      user_nodes.append(key)


  #Iterates until the routers are in the correct order, this makes sure that it is accurate
  finished = False
  while True:
    for route in attackers_routes:
      for i in range(len(route)-1):
        if packets_marked[route[i]] >= packets_marked[route[i+1]]:
          finished = False
          break
        else:
          finished = True
      if not finished:
        break
    #Checks if attackers have sent a greater number of packets than any innocent routers
    for attacker in attackers:
      for user_node in user_nodes:
        if packets_marked[user_node] >= packets_marked[attacker]*rate:
          finished = False
          break
      if not finished:
        break
    if finished:
      break
      
    
    #Sends the packets
    for user in users:
      to_be_marked = ""
      num_packets+=1
      current_packet = user

      #Traverses graph from user to victim
      while "V" != current_packet:
        if random.random() < probability:
          to_be_marked = current_packet
        current_packet = graph[current_packet]
      if to_be_marked != "":
        packets_marked[to_be_marked] += 1

    for _ in  range(num_users*rate//num_attackers):
      for attacker in attackers:
        to_be_marked = ""
        num_packets+=1
        current_packet = attacker

        #Traverses graph from user to victim
        while "V" != current_packet:
          if random.random() < probability:
            to_be_marked = current_packet
          current_packet = graph[current_packet]
        if to_be_marked != "":
          packets_marked[to_be_marked] += 1

  return packets_marked, num_packets

######################################################################################################################################################

def edge_sampling(graph, attackers, users, probability, rate):
  packets_marked = {}
  for key in graph:
    packets_marked[key + " | " + graph[key]] = 0

  #gets number of users and attackers
  num_users = len(users)
  num_attackers = len(attackers)

  #Puts the attackers' routes in a list in order
  attackers_routes = []
  for _ in range(len(attackers)):
    attackers_routes.append([])
  current_index = 0
  for attacker in attackers:
    current_attacker = attacker
    while "V" != current_attacker:
      attackers_routes[current_index].append(current_attacker + " | " + graph[current_attacker])
      current_attacker = graph[current_attacker]
    current_index+=1
  
  all_attackers =  [attacker for sublist in attackers_routes for attacker in sublist]
  user_nodes = []
  for key in graph:
    if key == "V":
      break
    current_edge = key + " | " + graph[key]
    if current_edge not in all_attackers:
      user_nodes.append(current_edge)


  num_packets = 0
  finished = False
  while True:
    for route in attackers_routes:
      for i in range(len(route)-1):
        if packets_marked[route[i]] >= packets_marked[route[i+1]]:
          finished = False
          break
        else:
          finished = True
      if not finished:
        break
    #Checks if attackers have sent a greater number of packets than any innocent routers
    for attacker in attackers:
      for user_node in user_nodes:
        if (packets_marked[user_node]+1)*rate >= packets_marked[attacker + " | " + graph[attacker]]:
          finished = False
          break
      if not finished:
        break
    if finished:
      break
      
    
    #Sends the packets
    for user in users:
      num_packets+=1
      current_packet = user
      to_be_marked = ""

      #Traverses graph from user to victim
      while "V" != current_packet:
        edge = current_packet+" | "+graph[current_packet]
        if random.random() < probability:
          to_be_marked = edge
        current_packet = graph[current_packet]
      if to_be_marked != "":
        packets_marked[to_be_marked] += 1

    for _ in range(num_users*rate//num_attackers):
      for attacker in attackers:
        to_be_marked = ""
        num_packets+=1
        current_packet = attacker

        #Traverses graph from user to victim
      while "V" != current_packet:
        edge = current_packet+" | "+graph[current_packet]
        if random.random() < probability:
          to_be_marked = edge
        current_packet = graph[current_packet]
      if to_be_marked != "":
        packets_marked[to_be_marked] += 1

  return packets_marked, num_packets



def get_users(graph, attackers):
  users = []
  for connection in graph:
    if 'U' in connection and connection not in attackers:
      users.append(connection)     
  return attackers, users  

def randomize_attacker(graph, num_attackers):
  attackers = []
  users = []
  for connection in graph:
    if 'U' in connection:
      users.append(connection)
  for _ in range(num_attackers):
    attacker = random.choice(users)
    users.remove(attacker)
    attackers.append(attacker)
  return attackers, users
  
  



probability = float(input("\nPacket market probability (0.2, 0.4, 0.5, 0.6, 0.8): "))
rate = int(input("Input x times more packets than the normal user the attacker should pump (x = 10, 100, 1000): "))
method = int(input("Input '0' for node sampling and '1' for edge sampling: "))
net = int(input("Input '3' for 3 branch network, '4' for 4 branch, and '5' for 5 branch: "))
num_attackers = int(input("Input the amount of attackers you want (should be less than number of branches): "))
print()

if net == 3:
  filename = "branch3.txt"
elif net == 4:
  filename = "branch4.txt"
else:
  filename = "branch5.txt"
graph = build_network(get_network(filename))
attackers, users = randomize_attacker(graph, num_attackers)
if method == 0:
  packets_marked, packets_sent = node_sampling(graph, attackers, users, probability, rate)
else:
  packets_marked, packets_sent = edge_sampling(graph, attackers, users, probability, rate)
packets_marked = sorted(packets_marked.items(), key=lambda x:x[1])
print(packets_marked)
print(packets_sent)

