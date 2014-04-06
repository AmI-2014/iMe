'''
Created on 06/apr/2014

@author: Andrea
'''

def close_files(): # Quick function to close every file used by main
    f_user.close()
    f_nerd.close()
    f_check.close()   
def username_update(): # Updates username when changed by rewriting username.txt
    f_user.seek(0)
    f_user.truncate()
    f_user.write(settings_list[0])    
def nerdmode_update(): # Updates NerdMode when changed by rewriting nerdmode.txt
    f_nerd.seek(0)
    f_nerd.truncate()
    f_nerd.write(settings_list[1])
def main_menu(): # Prints the main menu and returns the user choice
    return raw_input("MAIN MENU\nN - Create New Game\nP - Play a Game\nC - Manage Checkpoints\nS - Settings\nI - Info\nQ - Quit\nChoice: >")
def new_game(): # Creation of a new Treasure Hunt
    pass
def play_game(): # Start a new game using its ID
    game_id=raw_input("Enter game ID: >")
    pass
def manage_checkpoints(): # Uses the checkpoints.txt file to manage them 
    pass
def settings(): # Allow the user to change settings like username and nerdmode
    # Setting flag for settings menu loop until user wants to go back to main menu
    escape=0
    # Menu loop until going back
    while escape==0: 
        s_choice=raw_input("SETTINGS\nU - Set Player Username\nR - Reset Saved Checkpoints\nN - Enable/Disable \"Nerd\" Mode\nB - Back to Main Menu\nChoice: >")
        # Username change
        if s_choice=='U' or s_choice=='u': 
            settings_list[0]=raw_input("Insert Username: >")
            # username.txt update
            username_update() 
        # Resetting checkpoints
        elif s_choice=='R' or s_choice=='r': 
            f_check.seek(0)
            f_check.truncate()
        # Changing nerdmode
        elif s_choice=='N' or s_choice=='n': 
            settings_list[1]=raw_input("Insert 1 to enable Nerd Mode, 0 to Disable. >")
            # Avoiding bad choices
            while settings_list[1]!="0" and settings_list[1]!="1": 
                settings_list[1]=raw_input("Bad choice. Insert 1 to enable Nerd Mode, 0 to Disable. >")
            # nerdmode.txt update
            nerdmode_update() 
        # Back to main menu
        elif s_choice=='B' or s_choice=='b': 
            escape=1
        else:
            print "Invalid choice, try again."     
def info(): # Prints info about version and creators
    print ("Version 0.0.1\nCreated by iMe\n")

if __name__ == '__main__':
    # Setting main quit flag
    flag=0 
    # Opening useful files
    f_user=open("username.txt","r+")
    f_nerd=open("nerdmode.txt","r+")
    f_check=open("checkpoints.txt","r+")
    # Copying settings from files to a list for better use and edit properties
    settings_list=[f_user.read(),f_nerd.read()]
    # Menu loop until user wants to exit
    while flag==0:
        # main_menu returns user's choice
        choice=main_menu()
        if choice=='N' or choice=='n':
            # Calling function to start the creation module for a new game
            new_game()
        elif choice=='P' or choice=='p':
            # Calling function to play an existing game
            play_game()
        elif choice=='C' or choice=='c':    
            # Calling function to manage checkpoints
            manage_checkpoints()
        elif choice=='S' or choice=='s':    
            # Calling function to edit settings
            settings()
        elif choice=='I' or choice=='i':    
            # Calling function to print app informations
            info()
        elif choice=='Q' or choice=='q':  
            # Setting the escape flag to quit the app  
            flag=1
        else:   
            # Wrong input
            print "Invalid choice, try again."  
    # File closing before closing the app
    close_files()   