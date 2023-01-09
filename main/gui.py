import sys
from simplepygamemenus.menu import Menu
import pygame
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from run import create_image_from_stream

class GUI:

    def __init__(self, sizex, sizey):

        # d = pygame.Surface(size=(1000,800)
        cx = sizex/2
        cy = sizey/2

        self.main = Menu(displaytitle=False, x=sizex, y=sizey)
        self.main.add_text(text="THINKING ABOUT U", x=cx, y=30, size=25, color="#ff80ff")
        # b_menu = Menu(main=self.main, title="other menu", showESCKEYhint=True)
        # self.main.add_button(label="Connect", x=cx, y=250, fontsize=30, function=b_menu.run_menu)

    def connect_board(self, boardID):
        "Connect a board"
        self.board = BoardShim(boardID, self.params)
        self.board.prepare_session()

    def run_demo(self):
        BoardShim.enable_dev_board_logger()
        self.params = BrainFlowInputParams()
        self.connect_board(boardID=-1)
        self.run()

    def run_with_board(self, boardID, port):
        BoardShim.enable_dev_board_logger()
        self.params = BrainFlowInputParams()
        self.params.serial_port = port
        self.connect_board(boardID=boardID)
    
    def run(self, timesleep=60):
        self.board.start_stream()
        print(f"\nCollecting {timesleep} seconds of Brain Activity...\n")
        time.sleep(timesleep)
        print("DONE! Generating...")
        data = self.board.get_board_data()  # get all data and remove it from internal buffer
        self.board.stop_stream()
        self.board.release_session()

        create_image_from_stream(data=data, output_path="")


if __name__ == "__main__":
    # g = GUI(sizex=800, sizey=800)
    # g.main.add_button(label="DEMO", x=400, y=400, fontsize=30, function=g.run_demo)
    # g.main.run_menu()

    main = Menu()
    main.add_text(text="SIMPLE PYGAME MENUS", x=250, y=30, size=25)
    b_menu = Menu(main=main, title="other menu", showESCKEYhint=True)
    main.add_button(label="WHATS THIS?", x=250, y=250, fontsize=30, function=b_menu.run_menu)
    b_menu.add_button(label="exit", x=250, y=250, fontsize=30, function=sys.exit)

    next_menu = Menu(title="NEXT",main=b_menu)
    b_menu.add_button(label="next menu", x=250, y=400, fontsize=30, basecolor=(0,255,0), hovercolor=(255,255,255), function=next_menu.run_menu)


    main.run_menu()



