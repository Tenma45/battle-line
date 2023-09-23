import pygame
import sys
import game

def handle(event,components,client_socket,state,messages):

    hands, lanes, troop_rect, tactic_rect, start_button = components

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if state["status"] == "lobby":
            if start_button.collidepoint(event.pos):
                client_socket = game.join(state["port"],messages)
        else:
            if start_button.collidepoint(event.pos) and state["status"] == "Ready to start":
                game.start(client_socket)
            if troop_rect.collidepoint(event.pos) and state["status"] == "Draw a card":
                game.draw(client_socket,state,"troop")
            if tactic_rect.collidepoint(event.pos) and state["status"] == "Draw a card":
                game.draw(client_socket,state,"tactic")
            for hand in hands:
                card_rect, card = hand
                if card_rect.collidepoint(event.pos) and (state["status"] == "Select a card" or state["status"] == "Select a position"):
                    state["select_card"] = card
                    state["status"] = "Select a position"
            for lane in lanes[9:]:
                len_rect, index = lane
                third_card = state["board"][5][index-9] 
                if len_rect.collidepoint(event.pos) and state["status"] == "Select a position" and third_card == 0:
                    state["select_lane"] = index-9
                    game.place(client_socket,state)
                    index_hand = state["you"].index(state["select_card"])
                    state["you"][index_hand] = 0
                    state["status"] = "Draw a card"

    if event.type == pygame.KEYDOWN:

        # Check for backspace
        if event.key == pygame.K_BACKSPACE:
            # get text input from 0 to -1 i.e. end.
            state["port"] = state["port"][:-1]

        # Unicode standard is used for string
        # formation
        else:
            state["port"] += event.unicode
            if len(state["port"]) == 5:
                state["port"] += "/"

    return state, client_socket