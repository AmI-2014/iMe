'''
Created on 06/apr/2014

@author: Andrea
'''
import smtplib
from urllib import urlopen
from math import radians, fabs, sin, cos, acos
from random import shuffle, choice
from string import ascii_uppercase, digits
url="http://treasurehunting.altervista.org/server_checkpoints.txt"
email='treasurehuntingami@gmail.com'

def coordstr2rad(string): # Given a string of coordinates, returns a list with latitude and longitude in radians
    temp=string.split(",")
    coordinates=[]
    coordinates.append(radians(float(temp[0])))
    coordinates.append(radians(float(temp[1])))
    return coordinates
def distance_between_coordinates(str1,str2): # Given two strings of coordinates in radians, returns the distance between them in meters
    coord1=coordstr2rad(str1)
    coord2=coordstr2rad(str2)
    fi=fabs(coord1[1]-coord2[1])
    P = acos((sin(coord1[0]) * sin(coord2[0]))+(cos(coord1[0]) * cos(coord2[0]) * cos(fi)))
    return P*6372795.477598
def open_file(name): # Quick function to open or create files used by main
    try:
        f_new=open(name,"r+")
    except IOError:
        f_new=open(name,"w")
        f_new.close()
        f_new=open(name,"r+")
    return f_new
def starting_settings(settings_list): # First settings
    for i in range(0,3):
        if settings_list[i]=="":
            if i==0:
                settings_list[i]=raw_input("Write your username! >")
                username_update()
            elif i==1:
                choice="a"
                while choice!="y" and choice!="n" and choice!="Y" and choice!="N":
                    choice=raw_input("Do you want to use Bluetooth dongles for your checkpoints? (y/n) >")
                    if choice=="y" or choice=="Y":
                        settings_list[i]="1"
                    else:
                        settings_list[i]="0"
                nerdmode_update()
            elif i==2:
                settings_list[i]=raw_input("Write your Raspberry Pi IP: >")
                ip_update()
def close_files(): # Quick function to close every file used by main
    f_user.close()
    f_nerd.close()
    f_check.close()
    f_ip.close()
    f_server.close()
def username_update(): # Updates username when changed by rewriting username.txt
    f_user.seek(0)
    f_user.truncate()
    f_user.write(settings_list[0])    
def nerdmode_update(): # Updates NerdMode when changed by rewriting nerdmode.txt
    f_nerd.seek(0)
    f_nerd.truncate()
    f_nerd.write(settings_list[1])
def ip_update(): # Updates Raspberry IP when changed by rewriting raspberry_ip.txt
    f_ip.seek(0)
    f_ip.truncate()
    f_ip.write(settings_list[2])
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
def dictionary_to_game_file(f_out,check_dict,game_mode,sequential):
    f_out.seek(0)
    f_out.truncate()
    f_out.write(settings_list[0]+'\n'+game_mode+'\n'+sequential+'\n')
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
    check_number=int(raw_input("Insert the number of checkpoints you'd like: >"))
    game_mode=raw_input("Insert 1 for 'Guess final checkpoint' mode, 2 for normal mode: >")
    while game_mode!='1' and game_mode!='2':
        game_mode=raw_input("Bad input. Insert 1 for 'Guess final checkpoint' mode, 2 for normal mode: >")
    sequential=raw_input("Has everyone to follow the same path (1) or follow a random one (2)? >")
    while sequential!='1'and sequential!='2':
        sequential=raw_input("Bad input. Has everyone to follow the same path (1) or follow a random one (2)? >")
    max_range=int(raw_input("Insert max game range from your position (in meters): >"))
    player_position=get_gps_position()
    keys=server_checkpoints_dictionary.keys()
    shuffle(keys)
    game_checkpoints={}
    for key in keys:
        if check_number==0:
            break
        temp_coord=server_checkpoints_dictionary[key][1]
        if distance_between_coordinates(temp_coord,player_position)<=max_range:
            game_checkpoints[key]=server_checkpoints_dictionary[key]
            check_number-=1
    if check_number!=0:
        print "There weren't enough checkpoints. Try again."
    else:
        random_string=[]
        random_string.append("")
        random_string[0]=''.join(choice(ascii_uppercase + digits) for _ in range(0,6))
        game_file=open_file(random_string[0]+".txt")
        dictionary_to_game_file(game_file,game_checkpoints,game_mode,sequential)
        game_file.close()
        print "Game created! Its code is: "+random_string[0]                 
def new_normal_game():
    pass
def get_gps_position(): # For now dummy function to return gps positioning
    return "0.0,0.0"
def manage_checkpoints(): # Uses the checkpoints.txt file to manage them 
    # Setting flag for settings menu loop until user wants to go back to main menu
    escape=0
    # Menu loop until going back
    while escape==0: 
        c_choice=raw_input("MANAGE CHECKPOINTS\nV - View list of your local checkpoints\nP - View Properties of a single Checkpoint\nA - Add New Checkpoint\nE - Edit Checkpoint\nD - Delete Checkpoint\nS - Send Checkpoint suggestion\nB - Back to Main Menu\nChoice: >")
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
                    print ("Name: "+check_to_see+"\nCheckpoint Type: "+checkpoints_dictionary[check_to_see][0]+"\nBluetooth Key: "+checkpoints_dictionary[check_to_see][1]+"\nCheckpoint Trivia Hint (if present): "+checkpoints_dictionary[check_to_see][3]+"\n")
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
                new_check.append(raw_input("Insert Bluetooth Key: >"))
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
                    s_temp[0]=raw_input("Insert new Bluetooth Key (leave blank to let it the same ("+c_temp[1]+"): >")
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
        #Checkpoints suggestions    
        elif c_choice=='S' or c_choice=='s': 
            check_to_send=raw_input("Insert checkpoint name (case sensitive!) or number: >")
            try:
                check_to_send=index_to_checkpoint(int(check_to_send))
            except ValueError:
                pass
            try:
                message=""
                for i in range(0,len(checkpoints_dictionary[check_to_send])):
                    message+=(checkpoints_dictionary[key][i]+'\n')
                sendemail(check_to_send,message)
                print("Suggestion sent!\n")
            except KeyError:
                print("Bad input.\n")
            except ValueError:
                print("Bad input.\n")
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
        s_choice=raw_input("SETTINGS\nU - Set Player Username\nR - Reset Saved Checkpoints\nN - Enable/Disable \"Nerd\" Mode\nI - Set Raspberry Pi IP\nB - Back to Main Menu\nChoice: >")
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
        # Changing Raspberry Pi IP
        elif s_choice=="i" or s_choice=="I":
            settings_list[2]=raw_input("Insert Raspberry Pi IP: >")
            # raspberry_ip.txt update
            ip_update()
        # Back to main menu
        elif s_choice=='B' or s_choice=='b': 
            escape=1
        else:
            print "Invalid choice, try again."     
def info(): # Prints info about version and creators
    print ("Version 0.0.1\nCreated by iMe\n")
def sendemail(subject, message,login=email,password='treasurehunting2014',smtpserver='smtp.gmail.com:587',from_addr=email, to_addr_list=[email], cc_addr_list=[""]): # Function to send a suggestion!
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    
if __name__ == '__main__':
    # Setting main quit flag
    flag=0 
    # Opening useful files, creates them if they don't exist
    f_user=open_file("username.txt")
    f_nerd=open_file("nerdmode.txt")
    f_check=open_file("checkpoints.txt")
    f_ip=open_file("raspberry_ip.txt")
    # Copying settings from files to a list for better use and edit properties
    settings_list=[f_user.read(),f_nerd.read(),f_ip.read()]
    starting_settings(settings_list)
    # Copying checkpoints to a dictionary for better use and edit properties
    checkpoints_dictionary=checkpoints_file_to_dict(f_check)
    # Downloading the server's checkpoints file, opening it and copying it to a dictionary
    f_server=open_file("server_checkpoints.txt")
    f_server.seek(0)
    f_server.truncate()
    f_server.write(urlopen(url).read())
    server_checkpoints_dictionary=checkpoints_file_to_dict(f_server)
    # Menu loop until user wants to exit
    while flag==0:
        # main_menu returns user's choice
        m_choice=main_menu()
        if m_choice=='N' or m_choice=='n':
            # Calling function to start the creation module for a new game
            new_game()
        elif m_choice=='P' or m_choice=='p':
            # Calling function to play an existing game
            play_game()
        elif m_choice=='C' or m_choice=='c':    
            # Calling function to manage checkpoints
            manage_checkpoints()
        elif m_choice=='S' or m_choice=='s':    
            # Calling function to edit settings
            settings()
        elif m_choice=='I' or m_choice=='i':    
            # Calling function to print app informations
            info()
        elif m_choice=='Q' or m_choice=='q':  
            # Setting the escape flag to quit the app  
            flag=1
        else:   
            # Wrong input
            print "Invalid choice, try again."  
    # File closing before closing the app
    close_files()