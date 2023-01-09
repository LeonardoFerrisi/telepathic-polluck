import time

from connect import Comms
from user_interface_methods import dislay_console, dislay_input_console
from create import create_image_from_eeg, create_image_from_stream

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from simplepygamemenus.menu import Menu
import pandas as pd

class TAU:
    """
    Thinking About U:
        A condensed, more interactive version of telepathic polluck
    """
    def __init__(self):
        
        pass

    def preflight(self):
        """
        Conducts all processes neccessary for Brain Activity to Image Generation
        """
        pass
    
    def run(self):
        
        dislay_console(label="[TAU]", msg="Welcome to the Telepathic Polluck Demo! ", color='cyan')
        time.sleep(1)

        in1 = 0
        requestedVals = ["1","2"]
        while in1 not in requestedVals:
            in1 = dislay_input_console(label="[TAU]", msg="Would you like to:\n[1] Use a Previous EEG Recording\n[2] Record new EEG data\n", color='white')
            print(str(type(in1))+":"+in1)
            if in1 not in requestedVals:
                dislay_console(label="[TAU]", msg="Please enter either 1 or 2 to indicate selected option", color='red')

        if in1 == str(1):
            filepath = dislay_input_console(label="[TAU]", msg="Please enter the filepath of the recording you would like to use.", color="white")
            output_path = dislay_input_console(label="[TAU]", msg="Please enter the output directory path. Press enter to use default 'images/'.", color="white")
            self.run_filebased_image_gen(filepath, output_path)
        elif in1 == str(2):
            boardID = dislay_input_console(label="[TAU]", msg="Input ID of board to connect to", color="white")
            output_path = dislay_input_console(label="[TAU]", msg="Please enter the output directory path. Press enter to use default 'images/generated'.", color="white")
            
            # Connect board
            BoardShim.enable_dev_board_logger()
            params = BrainFlowInputParams()
            if int(boardID) > 0 :
                port = dislay_input_console(label="[TAU]", msg="Input ID of board to connect to", color="white")
                params.serial_port = port
            board = BoardShim(int(boardID), params)
            board.prepare_session()
            

            board.start_stream()
            print(f"\nCollecting 60 seconds of Brain Activity...\n")
            time.sleep(10)
            print("DONE! Generating...")
            data = board.get_board_data()  # get all data and remove it from internal buffer
            board.stop_stream()
            board.release_session()

            print(pd.DataFrame(data=data))

            self.image_gen_from_local_data(data=data, output_path="")
    
    def run_filebased_image_gen(self, filepath, output_path):
        """
        A method for loading an EEG recording file and outputting it
        """
        outpath = 'images/' if output_path == '' else output_path
        dislay_console(label="[TAU]", msg=f"Using '{outpath}' as output path", color='cyan')
        create_image_from_eeg(filename=filepath, output_dir=output_path)

    def image_gen_from_local_data(self, data, output_path):
        """
        A method for loading an EEG recording file and outputting it
        """
        outpath = 'images/generated/' if output_path == '' else output_path
        # dislay_console(label="[TAU]", msg=f"Using '{outpath}' as output path", color='cyan')
        print("[TAU]"+ f"  Using '{outpath}' as output path")
        create_image_from_stream(data=data, output_dir=output_path)

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

        create_image_from_stream(data=data, output_dir="")

if __name__ == "__main__":
    t = TAU()
    t.run()

    # g = GUI(sizex=800, sizey=800)
    # g.main.add_button(label="DEMO", x=400, y=400, fontsize=30, function=g.run_demo)
    # g.main.run_menu()

        


        


