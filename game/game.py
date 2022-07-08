import os
import time

from ai.state_for_machine import StateForMachine
from config import DEVELOPER_MODE
from constants import Role, HELP, BOARDS
from core.errors import RuleViolatedError
from game.errors import LosingGameError
from game.state_for_mankind import StateForMankind
from ai.tree_searcher import TreeSearcher


BOARD_MAP_FOR_HUMAN_ROLES = {
    Role.OFFENSIVE: BOARDS["OFFENSIVE"],
    Role.DEFENSIVE: BOARDS["DEFENSIVE"]
}


FOOL_PROOFER = TreeSearcher(1)
REFEREE = TreeSearcher(2)
AI = TreeSearcher(4)


class Game:
    def __init__(self, role=Role.OFFENSIVE, board=None):
        while role is None:
            role_ = input("Which role do you prefer: OFFENSIVE or DEFENSIVE? \n")
            try:
                role = Role[role_]
            except KeyError:
                print("invalid choice, please input again. ")
        if board is None:
            if board := os.environ.get("BOARD"):
                board = BOARDS[board]
            else:
                board = BOARD_MAP_FOR_HUMAN_ROLES[role]
        self._play_modes = {Role.OFFENSIVE: self._machine_move, Role.DEFENSIVE: self._machine_move, role: self._mankind_move}
        self._history = []
        self._winner = None
        self._state = StateForMankind(board, next_side=Role.OFFENSIVE)

    def play(self):
        print(f"Welcome to Chinese Chess! ")
        print(self._state.display)
        while self._winner is None:
            side = self._state.next_side
            if REFEREE.top_score(self._state.board, self._state.next_side) == 0:
                self._winner = side.opponent
                break
            if move := self._play_modes[side]():
                self._history.append(self._state.board)
                self._state = move
                print(move.display)
            else:
                print(f"{side} resigned. ")
                self._winner = side.opponent
            if DEVELOPER_MODE:
                print(f"cache hit: {StateForMachine.HIT}")
                print(f"cache miss: {StateForMachine.MISS}")
                print(f"cache size: {len(StateForMachine.CACHE)}")
        print(f"Winner: {self._winner}")

    def _mankind_move(self):
        while True:
            command = input(f"please input your next move: ")
            if command.lower() == "resign":
                return
            if command.lower() == "revert":
                if len(self._history) >= 2:
                    self._history.pop()
                    self._state = StateForMankind(self._history.pop(), self._state.next_side)
                    print("Reverted to two steps before. ")
                    print(self._state.display)
                else:
                    print("Unable to revert. ")
                continue
            if command == 'help' or len(command) not in (4, 5):
                print(HELP)
                continue
            try:
                vector = self._state.parse_command(command)
                vector = self._state.is_valid(vector)
                result = self._state.create_from_vector(vector)
                if FOOL_PROOFER.top_score(result.board, result.next_side) == float('inf'):
                    raise LosingGameError
                return result
            except (RuleViolatedError, LosingGameError) as err:
                print(err)
                print("Enter --help or -h for help. ")
                continue

    def _machine_move(self):
        print("Machine is thinking...")
        time_s = time.time()
        result = AI.strategy(self._state.board, self._state.next_side)
        time_e = time.time()
        if DEVELOPER_MODE:
            print(f"Time: {time_e-time_s}")
        return result