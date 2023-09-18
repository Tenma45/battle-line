import pygame
import renderer
import socket_handler
import event_handler
import game
from queue import Queue

# Create a clock to control frame rate
clock = pygame.time.Clock()

# Initialize the client socket
messages = Queue()
client_socket = None

# Main loop

state = {
    "board":[[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]],
    "pins":[0,0,0,0,0,0,0,0,0],
    "enemy":[0,0,0,0,0,0],
    "you":[0,0,0,0,0,0],
    "troop":60,
    "tactic":10,
    "status":"lobby",
    "player":0,
    "select_card":0,
    "select_lane":0,
    "result":"",
    "port":""
}

while True:

    status = state["status"]

    # Render and display the message
    state = game.update_from_server(messages,state)

    if(status == "lobby"):
        components = renderer.lobby(state)
    else:
        components = renderer.render(state)

    temp = client_socket
    for event in pygame.event.get():
        state, client_socket = event_handler.handle(event,components,client_socket,state,messages)
    if temp != client_socket:
        print(temp,"=>",client_socket)
    

    pygame.display.flip()
    clock.tick(30)

# Close the client socket when the game ends
client_socket.close()
