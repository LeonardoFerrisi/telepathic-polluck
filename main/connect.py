import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets

class Comms:
    """
    A class for handling connections to boards
    """
    def __init__(self):
        pass

class Board:
    """
    Class for using boards
    """
    def __init__(self, id=-1, port=""):
        BoardShim.enable_dev_board_logger()
        self.params = BrainFlowInputParams()
        self.params.serial_port = port
        self.board = BoardShim(id, self.params)
        self.board.prepare_session()

    def run_for(self, timesleep=60):
        self.board.start_stream()
        print(f"\nCollecting {timesleep} seconds of Brain Activity...\n")
        time.sleep(timesleep)
        print("DONE! Generating...")
        data = self.board.get_board_data()  # get all data and remove it from internal buffer
        self.board.stop_stream()

        return data

    def release(self):
        self.board.release_session()

    def prepare(self):
        self.board.prepare_session()