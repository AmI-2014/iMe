'''
Created on 06/apr/2014

@author: Andrea
'''
def open_file(name): # Quick function to open or create files used by main
    try:
        f_new=open(name,"r+")
    except IOError:
        f_new=open(name,"w")
        f_new.close()
        f_new=open(name,"r+")
    return f_new
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
def create_game_file(): # Creates the new game file to be uploaded to the server
    pass
def read_game_file(): # Reads a game file and copies its content in memory
    pass
def checkpoints_file_to_dict(f_in): # Copies checkpoints from a file to a dictionary for a better use, returning the dictionary itself
    check_dict={}
    for line in f_in:
        # Every checkpoint name is defined by an asterisk char before it
        if line[0]=='*': 
            ntemp=line.replace('*','')
            temp=ntemp.replace('\n','')
            check_dict[temp]=[]
        else:
            check_dict[temp].append(line.replace('\n',''))
    return check_dict
def checkpoints_dict_to_file(f_out,check_dict): # Copies checkpoints from a dictionary to a file
    f_out.seek(0)
    f_out.truncate()
    for key in check_dict:
        f_out.write('*'+key+'\n')
        for i in range(0,len(check_dict[key])):
            f_out.write(check_dict[key][i]+'\n')
def main_menu(): # Prints the main menu and returns the user choice
    return raw_input("MAIN MENU\nN - Create New Game\nP - Play a Game\nC - Manage Checkpoints\nS - Settings\nI - Info\nQ - Quit\nChoice: >")
def new_game(): # Creation of a new Treasure Hunt, either fully randomized or not
    escape=0
    # Menu loop until going back
    while escape==0: 
        g_choice=raw_input("NEW GAME\nR - New Random Game\nN - New Normal Game\nB - Back to Main Menu\nChoice: >")
        # New Random Game
        if g_choice=='R' or g_choice=='r': 
            new_random_game() 
        # New Non-Random Game
        elif g_choice=='N' or g_choice=='n': 
            new_normal_game()
        # Back to main menu
        elif g_choice=='B' or g_choice=='b': 
            escape=1
        else:
            print "Invalid choice, try again."     
def play_game(): # Start a new game using its ID
    pass
def new_random_game():
    pass
def new_normal_game():
    pass
def manage_checkpoints(): # Uses the checkpoints.txt file to manage them 
    # Setting flag for settings menu loop until user wants to go back to main menu
    escape=0
    # Menu loop until going back
    while escape==0: 
        c_choice=raw_input("MANAGE CHECKPOINTS\nV - View list of your local checkpoints\nP - View Properties of a single Checkpoint\nA - Add New Checkpoint\nE - Edit Checkpoint\nD - Delete Checkpoint\nB - Back to Main Menu\nChoice: >")
        # Print checkpoints list
        if c_choice=='V' or c_choice=='v': 
            i=1
            for key in checkpoints_dictionary:
                print(str(i)+". "+key)
                i+=1
        # View properties of a single checkpoint
        elif c_choice=='P' or c_choice=='p': 
            check_to_see=raw_input("Insert checkpoint name (case sensitive!) or number: >")
            # Avoiding errors and using different layouts for GPS and physical checkpoints
            try:
                check_to_see=index_to_checkpoint(int(check_to_see))
            except ValueError:
                pass
            try:
                # Printing properties             
                if check_to_see!='0' and checkpoints_dictionary[check_to_see][0]=="GPS":
                    print ("Name: "+check_to_see+"\nCheckpoint Type: "+checkpoints_dictionary[check_to_see][0]+"\nCheckpoint Coordinates: "+checkpoints_dictionary[check_to_see][1]+"\nCheckpoint proximity class: "+checkpoints_dictionary[check_to_see][2]+"\nCheckpoint Trivia Hint (if present): "+checkpoints_dictionary[check_to_see][3]+"\n")    
                elif check_to_see!='0':
                    print ("Name: "+check_to_see+"\nCheckpoint Type: "+checkpoints_dictionary[check_to_see][0]+"\nRaspberry Pi IP: "+checkpoints_dictionary[check_to_see][1]+"\nCheckpoint Trivia Hint (if present): "+checkpoints_dictionary[check_to_see][3]+"\n")
                else:
                    print('Bad input.\n')
            except KeyError:
                print("Bad input.\n")
            except ValueError:
                print("Bad input.\n")
        # Add New Checkpoint
        elif c_choice=='A' or c_choice=='a':
            new_check=[] 
            new_check_name=raw_input("Insert Checkpoint Name: >")
            # Just a lot of questions by the program and answers by the user, nothing much
            # If NerdMode is ON, asking type of checkpoint. Else, setting it to GPS.
            if settings_list[1]=="1":
                new_check.append(raw_input("Insert Checkpoint Type (1 for GPS, 2 for Physical): >"))
                while new_check[0]!="1" and new_check[0]!="2":
                    new_check[0]=raw_input("Wrong Input. Insert Checkpoint Type (1 for GPS, 2 for Physical): >")
                if new_check[0]=="1":
                    new_check[0]="GPS"
                else:
                    new_check[0]="Physical"
            else:
                new_check.append("GPS")
            if new_check[0]=="GPS":
                new_check.append(raw_input("Insert Checkpoint Coordinates: >"))
            else:
                new_check.append(raw_input("Insert Raspberry Pi IP: >"))
            if new_check[0]=="GPS":
                new_check.append(raw_input("Insert Checkpoint Proximity Class (0: <10mt, 1: <25mt, 2: <100mt, 3: <1km, 4: <10km: >"))
            else:
                new_check.append("0")
            while new_check[2]!="0" and new_check[2]!="1" and new_check[2]!="2" and new_check[2]!="3" and new_check[2]!="4":
                new_check[2]=raw_input("Wrong Input. Insert Checkpoint Proximity Class (0: <10mt, 1: <25mt, 2: <100mt, 3: <1km, 4: <10km): >")
            new_check.append(raw_input("Insert Checkpoint Trivia Question (if wanted): >"))
            checkpoints_dictionary[new_check_name]=new_check
            checkpoints_dict_to_file(f_check,checkpoints_dictionary)
        # Edit existing Checkpoint
        elif c_choice=='E' or c_choice=='e':
            check_to_see=raw_input("Insert checkpoint name (case sensitive!) or number: >")
            # Avoiding errors and using different layouts for GPS and physical checkpoints
            try:
                check_to_see=index_to_checkpoint(int(check_to_see))
            except ValueError:
                pass
            try:                
                # Using a list, easier to use an can be modified. Copying in it each property of the checkpoint to be edited, then the checkpoint is popped from the dictionary
                c_temp=[]
                c_temp.append(checkpoints_dictionary[check_to_see][0])
                c_temp.append(checkpoints_dictionary[check_to_see][1])
                c_temp.append(checkpoints_dictionary[check_to_see][2])
                c_temp.append(checkpoints_dictionary[check_to_see][3])
                checkpoints_dictionary.pop(check_to_see)
                s_temp=[]
                # Again, just a bunch of questions and answers
                s_temp.append(raw_input("Insert new name (leave blank to let it the same ("+check_to_see+"): >"))
                if s_temp[0]!="":
                    new_name=s_temp[0]
                else:
                    new_name=check_to_see
                if settings_list[1]=="1":
                    s_temp[0]=raw_input("Insert new type (leave blank to let it the same ("+c_temp[0]+") (1 for GPS, 2 for Physical): >")
                    while s_temp[0]!="1" and s_temp[0]!="2" and s_temp[0]!="":
                        s_temp[0]=raw_input("Bad Input. Insert new type (leave blank to let it the same ("+c_temp[0]+") (1 for GPS, 2 for Physical): >")
                    if s_temp[0]=="1":
                        c_temp[0]="GPS"
                    elif s_temp[0]=="2":
                        c_temp[0]="Physical"
                if c_temp[0]=="GPS":
                    s_temp[0]=raw_input("Insert new coordinates (leave blank to let it the same ("+c_temp[1]+"): >")
                    if s_temp[0]!="":
                        c_temp[1]=s_temp[0]
                else:
                    s_temp[0]=raw_input("Insert new Raspberry Pi IP (leave blank to let it the same ("+c_temp[1]+"): >")
                    if s_temp[0]!="":
                        c_temp[1]=s_temp[0]
                if c_temp[0]=="GPS":
                    s_temp[0]=raw_input("Insert new Checkpoint Proximity Class (leave blank to let it the same ("+c_temp[2]+") (0: <10mt, 1: <25mt, 2: <100mt, 3: <1km, 4: <10km): >")
                    while s_temp[0]!="0" and s_temp[0]!="1" and s_temp[0]!="2" and s_temp[0]!="3" and s_temp[0]!="4" and s_temp[0]!="":
                        s_temp[0]=raw_input("Bad input. Insert new Checkpoint Proximity Class (leave blank to let it the same ("+c_temp[2]+") (0: <10mt, 1: <25mt, 2: <100mt, 3: <1km, 4: <10km): >")
                    if s_temp[0]!="":
                        c_temp[2]=s_temp[0]
                s_temp[0]=raw_input("Insert new Trivia Hint (leave blank to let it the same ("+c_temp[3]+"), write 0 to delete: >")
                if s_temp[0]=="0":
                    c_temp[3]=""
                elif s_temp[0]!="":
                    c_temp[3]=s_temp[0]
                checkpoints_dictionary[new_name]=c_temp
            except KeyError:
                print("Bad input.\n")
            except ValueError:
                print("Bad input.\n")
            checkpoints_dict_to_file(f_check,checkpoints_dictionary)
        elif c_choice=='D' or c_choice=='d':
            check_to_see=raw_input("Insert checkpoint name (case sensitive!) or number: >")
            # Avoiding errors and using different layouts for GPS and physical checkpoints
            try:
                check_to_see=index_to_checkpoint(int(check_to_see))
            except ValueError:
                pass
            try:
                checkpoints_dictionary.pop(check_to_see)
            except KeyError:
                print("Bad input.\n")
            except ValueError:
                print("Bad input.\n")
            checkpoints_dict_to_file(f_check,checkpoints_dictionary)
        # Back to main menu
        elif c_choice=='B' or c_choice=='b': 
            escape=1
        else:
            print "Invalid choice, try again."     
def index_to_checkpoint(index): # Given an int, returns the key of the checkpoint dictionary with that index, or "0" if index is negative or too large
    i=1
    for key in checkpoints_dictionary:
        if i==index:
            return key
        else:
            i+=1
    return "0"
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
            checkpoints_dictionary.clear()
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
    # Opening useful files, creates them if they don't exist
    f_user=open_file("username.txt")
    f_nerd=open_file("nerdmode.txt")
    f_check=open_file("checkpoints.txt")
    # Copying settings from files to a list for better use and edit properties
    settings_list=[f_user.read(),f_nerd.read()]
    # Copying checkpoints to a dictionary for better use and edit properties
    checkpoints_dictionary=checkpoints_file_to_dict(f_check)
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