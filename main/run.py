import time

from connect import Comms
from user_interface_methods import dislay_console, dislay_input_console
from create import create_image_from_eeg

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
            dislay_input_console(label="[TAU]", msg="UNDER CONSTRUCTION, will prompt for boards to connect to", color="white")
    
    def run_filebased_image_gen(self, filepath, output_path):
        """
        A method for loading an EEG recording file and outputting it
        """
        outpath = 'images/' if output_path == '' else output_path
        dislay_console(label="[TAU]", msg=f"Using '{outpath}' as output path", color='cyan')
        create_image_from_eeg(filename=filepath, output_dir=output_path)
    
if __name__ == "__main__":
    t = TAU()
    t.run()

        


        


