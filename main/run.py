import time

from connect import Comms
from user_interface_methods import dislay_console, display_input_console
from create import create_image_from_eeg, create_image_from_stream

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from simplepygamemenus.menu import Menu
import pandas as pd

from alive_progress import alive_bar
import time
import os

class TAU:
    """
    Thinking About U:
        A condensed, more interactive version of telepathic polluck
    """
    def __init__(self):
        
        self.board_code_pairs = {
            "0" : -1,  # Simulated board
            "1" : 22,  # Muse 2 Board using BLED Dongle
            "2" : 23,  # Muse 2016 Board using BLED Dongle
        }

        self.board_code_name_pairs = {
            "0": "Simulated Board",
            "1": "Muse 2",
            "2": "Muse 2016"
        }

    def preflight(self):
        """
        Conducts all processes neccessary for Brain Activity to Image Generation
        """
        pass

    def board_prompt(self):
        """
        Prompt the user to select a desired board
        """
        dislay_console( label="TAU", msg="The following are boards you can use: ", color="cyan")
        for key, value in self.board_code_name_pairs.items():
            dislay_console( label=key, msg=value )

        print("\n")

        boardID = 100 # start with a ridiculous value

        while boardID not in self.board_code_pairs.keys():
            boardID = display_input_console(label="[TAU]", msg="Input ID of board to connect to", color="white")

            if boardID not in self.board_code_pairs.keys():
                dislay_console(label="WARNING", msg="boardID not in stored values. Please try again.", color="red")

        return self.board_code_pairs[boardID]

    def port_prompt(self):
        """
        Prompt the user to enter a new port or use the current one
        """
        data = self.read_userdata()
        port = data["PORT"]
        dislay_console(label="[TAU]", msg=f"Current port is: {port}")
        changeport = display_input_console(label="[TAU]", msg="Would you like to change this port? (Y/N)")
        if changeport.upper() == "Y":
            dislay_console(label="[ HINT ]", msg="You can find which ports are available in DEVICE MANAGER")
            port = display_input_console(label="[TAU]", msg="Input port:", color="white")
            self.update_userdata("PORT", port)
        return port

    def read_userdata(self):
        """
        Reads the contents of local_data/userdata.dat
        """
        data = {}
        with open("main//local_data//userdata.dat", "r") as f:
            for line in f.readlines():
                var, val = line.split(": ")
                data[var] = val
        return data

    def update_userdata(self, variable:str, value):

        # assert that variable exists

        data = self.read_userdata()

        # wipe the file

        open("main//local_data//userdata.dat", "w").close()

        assert variable.upper() in data.keys()

        # change it 

        data[variable] = str(value)

        with open("main//local_data//userdata.dat", "w") as f:
            for key, value in data.items():
                content = key.upper() + ": " + value
                f.writelines(content)
    
    def run(self):
        
        dislay_console(label="[TAU]", msg="Welcome to the Telepathic Polluck Demo! ", color='cyan')
        time.sleep(1)

        in1 = 0
        requestedVals = ["1","2"]
        while in1 not in requestedVals:
            in1 = display_input_console(label="[TAU]", msg="Would you like to:\n[1] Use a Previous EEG Recording\n[2] Record new EEG data\n", color='white')
            print(str(type(in1))+":"+in1)
            if in1 not in requestedVals:
                dislay_console(label="[TAU]", msg="Please enter either 1 or 2 to indicate selected option", color='red')

        if in1 == str(1):
            filepath = display_input_console(label="[TAU]", msg="Please enter the filepath of the recording you would like to use.", color="white")
            output_path = display_input_console(label="[TAU]", msg="Please enter the output directory path. Press enter to use default 'images/'.", color="white")
            self.run_filebased_image_gen(filepath, output_path)
        elif in1 == str(2):
            boardID = self.board_prompt()
            output_path = display_input_console(label="[TAU]", msg="Please enter the output directory path. Press enter to use default 'images/generated'.", color="white")
            
            # Connect board
            BoardShim.enable_dev_board_logger()
            params = BrainFlowInputParams()
            if int(boardID) > 0 :
                port = self.port_prompt()
                params.serial_port = port
            board = BoardShim(int(boardID), params)
            board.prepare_session()
            
            TIMESLEEP = display_input_console(label="[TAU]", msg="How many seconds of brain activity do you want to record? Press ENTER for default 60", color="white")

            if TIMESLEEP == "": TIMESLEEP = 60

            board.start_stream()
            print(f"\nCollecting {int(TIMESLEEP)} seconds of Brain Activity...\n")

            with alive_bar(int(TIMESLEEP)) as bar:
                for i in range(int(TIMESLEEP)):
                    time.sleep(1.0)
                    bar()

            print("DONE! Generating...")
            data = board.get_board_data()  # get all data and remove it from internal buffer
            board.stop_stream()
            board.release_session()

            # print(pd.DataFrame(data=data)) # For debugging purposes

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
        username = display_input_console(label="[TAU]", msg="Please enter the name for the image.", color="white")
        create_image_from_stream(data=data, output_dir=output_path, username=username)

if __name__ == "__main__":
    os.system('cls')
    t = TAU()
    t.run()

        


