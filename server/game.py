import pickle
import random
import time
import math
import copy

initial_state = {
    "board": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
    "pins": [0, 0, 0, 0, 0, 0, 0, 0, 0],
    "enemy": [0, 0, 0, 0, 0, 0, 0],
    "you": [0, 0, 0, 0, 0, 0, 0],
    "troop": [i for i in range(1, 61)],
    "tactic": [i for i in range(61, 71)],
    "player1":
    None,
    "player2":
    None,
    "result":
    ""
}

state = {}

players = {"player1": None, "player2": None}


def init(connected_clients, client_socket):
  number_of_player = len(connected_clients)
  data = {"action": "init", "player": number_of_player}
  if number_of_player == 1:
    players["player1"] = client_socket
    state["player1"] = client_socket
  if number_of_player == 2:
    players["player2"] = client_socket
    state["player2"] = client_socket
  for connected_client in connected_clients:
    send_data(connected_client, data)


def start():
  state["board"] = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
  state["pins"] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
  state["enemy"] = [0, 0, 0, 0, 0, 0, 0]
  state["you"] = [0, 0, 0, 0, 0, 0, 0]
  state["troop"] = [i for i in range(1, 61)]
  state["tactic"] = [i for i in range(61, 71)]
  state["result"] = ""
  state["player1"] = players["player1"]
  state["player2"] = players["player2"]
  random.shuffle(state["troop"])
  random.shuffle(state["tactic"])
  data = {
      "action": "start",
  }
  send_data(state["player1"], data)
  send_data(state["player2"], data)
  for _ in range(6):
    time.sleep(0.5)
    draw({"player": 1, "deck": "troop"})
    draw({"player": 2, "deck": "troop"})
  time.sleep(0.5)
  data = {"action": "update_status", "status": "Select a card"}
  send_data(state["player1"], data)
  data = {"action": "update_status", "status": "Opponent's turn"}
  send_data(state["player2"], data)


def draw(data):
  client = state["player1"] if data["player"] == 1 else state["player2"]
  opponent = state["player2"] if data["player"] == 1 else state["player1"]
  if data["deck"] == "troop":
    if len(state["troop"]) == 0:
      card = 0
      back_card = 0
    else:
      card = state["troop"].pop()
      back_card = 1
  else:
    if len(state["tactic"]) == 0:
      card = 0
      back_card = 0
    else:
      card = state["tactic"].pop()
      back_card = 2
  data_to_send = {"action": "draw", "card": card}
  send_data(client, data_to_send)

  data_to_send = {"action": "opponent_draw", "card": back_card}
  send_data(opponent, data_to_send)


def place(data):
  card = data["card"]
  lane = data["lane"]
  player = data["player"]
  if player == 1:
    first_card = state["board"][0][lane]
    second_card = state["board"][1][lane]
    third_card = state["board"][2][lane]
    if first_card == 0:
      state["board"][0][lane] = card
    elif second_card == 0:
      state["board"][1][lane] = card
    elif third_card == 0:
      state["board"][2][lane] = card
  if player == 2:
    first_card = state["board"][3][lane]
    second_card = state["board"][4][lane]
    third_card = state["board"][5][lane]
    if first_card == 0:
      state["board"][3][lane] = card
    elif second_card == 0:
      state["board"][4][lane] = card
    elif third_card == 0:
      state["board"][5][lane] = card
  board_player1_view = [
      state["board"][3], state["board"][4], state["board"][5],
      state["board"][0], state["board"][1], state["board"][2]
  ]
  board_player2_view = state["board"]
  data = {"action": "place", "board": board_player1_view}
  send_data(state["player1"], data)
  data = {"action": "place", "board": board_player2_view}
  send_data(state["player2"], data)
  check_pin(lane, player)


def check_pin(lane, player):
  cards = []
  for pos in range(6):
    card = state["board"][pos][lane]
    cards.append(card)
  if 0 not in cards:
    player1_value = calculate_value(cards[:3])
    player2_value = calculate_value(cards[3:])
    print("player1:", player1_value, " vs ", "player2: ", player2_value)
    if player1_value > player2_value:
      state["pins"][lane] = 1
    elif player1_value < player2_value:
      state["pins"][lane] = 2
    elif player1_value == player2_value:
      opponent_player = 2 if player == 1 else 1
      state["pins"][lane] = opponent_player
    pins_player1_view = state["pins"]
    data = {"action": "update_pins", "pins": pins_player1_view}
    send_data(state["player1"], data)
    send_data(state["player2"], data)
    check_result()


def calculate_value(cards):
  cards_number = [10 if item % 10 == 0 else item % 10 for item in cards]
  cards_color = list(map(lambda card: math.floor((card - 1) / 10), cards))
  is_same_color = len(set(cards_color)) == 1
  is_three_of_a_kind = len(set(cards_number)) == 1
  is_running_number = sorted(cards_number) == list(
      range(min(cards_number),
            max(cards_number) + 1))
  value = 0
  if is_running_number and is_same_color:
    value = 70
  elif is_three_of_a_kind:
    value = 60
  elif is_same_color:
    value = 50
  elif is_running_number:
    value = 40
  else:
    value = sum(cards_number)  # max 30
  return value


def check_result():
  player1_pins = state["pins"].count(1)
  player2_pins = state["pins"].count(2)
  for i in range(7):
    three_cons_pins = state["pins"][i:i + 3]
    is_player1_get_three_cons_pins = len(list(
        set(three_cons_pins))) == 1 and three_cons_pins[0] == 1
    is_player2_get_three_cons_pins = len(list(
        set(three_cons_pins))) == 1 and three_cons_pins[0] == 2
    if is_player1_get_three_cons_pins or is_player2_get_three_cons_pins:
      break
  winner = 1 if (
      player1_pins >= 5 or is_player1_get_three_cons_pins) else 2 if (
          player2_pins >= 5 or is_player2_get_three_cons_pins) else 0
  if winner != 0:
    data = {"action": "update_result", "winner": winner}
    send_data(state["player1"], data)
    send_data(state["player2"], data)


def send_data(socket, data):
  dumped = pickle.dumps(data)
  message_length = len(dumped).to_bytes(
      4, byteorder='big')  # 4 bytes for message length
  final_message = message_length + dumped
  socket.send(final_message)


def update(connected_clients, client_socket, data):
  action = data["action"]
  if action == "start":
    start()
  if action == "draw":
    draw(data)
  if action == "place":
    place(data)
