import socket_handler
import pickle

def update_from_server(messages,state):
    while not messages.empty():
        data = messages.get()
        print("Receive from server:",data)
        action = data["action"]
        if action == "init":
            number_of_player = data["player"]
            if state["player"] == 0:
                state["player"] = number_of_player
            if number_of_player == 1:
                state["status"] = "Waiting for opponent"
            elif number_of_player == 2:
                state["status"] = "Ready to start"
            else:
                state["status"] = "You are not allow to join room"
        if action == "start":
            state["you"] = [0,0,0,0,0,0]
            state["enemy"] = [1,1,1,1,1,1]    
            state["board"] = [[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]
            state["pins"] = [0,0,0,0,0,0,0,0,0]
            state["troop"] = 60
            state["tactic"] = 10
            state["result"] = ""
        if action == "draw":
            card = data["card"]
            index = state["you"].index(0)
            state["you"][index] = card
            deck = "troop" if card <= 60 else "tactic"
            state[deck] -= 1
            state["status"] = "Opponent's turn"
        if action == "opponent_draw":
            card = data["card"]
            # index = state["enemy"].index(0)
            # state["enemy"][index] = card    
            deck = "troop" if card == 1 else "tactic"
            state[deck] -= 1
            state["status"] = "Select a card"
        if action == "place":
            state["board"] = data["board"]
        if action == "update_pins":
            state["pins"] = data["pins"]
        if action == "update_result":
            state["result"] = "win" if data["winner"] == state["player"] else "lose"
            state["status"] = "Ready to start"

    return state

def start(client_socket):
    data = {"action":"start"}
    socket_handler.send_data_to_server(client_socket,data)

def place(client_socket,state):
    card = state["select_card"]
    lane = state["select_lane"]
    player = state["player"]
    data = {
        "action":"place",
        "card":card,
        "lane":lane,
        "player":player
        }
    socket_handler.send_data_to_server(client_socket,data)

def draw(client_socket,state,deck):
    data = {
        "action":"draw",
        "player": state["player"],
        "deck": deck
    }
    socket_handler.send_data_to_server(client_socket,data)

def join(port:str,messages):
    port_number = int(port.split('/')[0])
    server_number = port.split('/')[1]
    client_socket = socket_handler.connect(server_number,port_number,messages)
    return client_socket
