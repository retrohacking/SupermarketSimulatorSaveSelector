import glob
import os
import shutil
import subprocess

GAME_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Supermarket Simulator\\Supermarket Simulator.exe"
SAVE_PATH =  os.path.expanduser('~\\AppData\\LocalLow\\Nokta Games\\Supermarket Simulator')
SLOT_PATH =  os.path.expanduser('~\\AppData\\LocalLow\\Nokta Games\\Supermarket Simulator\\Slots')
AVAILABLE_OPTIONS = 4

def getmarketname(sf):
    with open(sf) as f:
        savefile = f.read()
        marketname=savefile.split("ShopName\" : \"")[-1].split("\"")[0]
        return marketname

def deletesavefile():
    savelist = glob.glob(SLOT_PATH+"\\*.es3")
    count=0
    print("Which slot do you want to delete?\n")
    for file in savelist:
        marketname = getmarketname(file)
        print("["+str(count)+"] "+file.split("\\")[-1]+" - "+marketname)
        count+=1

    choice = int(input("\n>"))
    while (choice not in range (0, count)):
        choice = int(input("Please insert a valid option\n>"))

    print("This action will delete "+savelist[choice].split("\\")[-1]+". Are you sure? [y/N]")
    delconfirm = input(">")
    if delconfirm=="y" or delconfirm=="Y":
        os.remove(savelist[choice])
        print (savelist[choice].split("\\")[-1] +" has been deleted. :(")
        input("Bye Bye!")
    else:
        print("Deletion has been cancelled.")
        input("Bye Bye!")


def saveslot(sf):
    savefiles = glob.glob(SAVE_PATH+"\\*.es3")
    latest_savefile = max(savefiles, key= os.path.getmtime)
    shutil.copy(latest_savefile, sf)
    print("New modifications, if any has been done, have been saved!")
    input("Bye Bye!")

def setsavefiletoload(sf):
    fileslist=glob.glob(SAVE_PATH+"\\*.es3")
    for file in fileslist:
        os.remove(file)
    shutil.copy(sf, SAVE_PATH)

def loadexistingsavefile():
    savelist = glob.glob(SLOT_PATH+"\\*.es3")
    count=0
    print("Which slot do you want to load?\n")
    for file in savelist:
        marketname = getmarketname(file)
        print("["+str(count)+"] "+file.split("\\")[-1]+" - "+marketname)
        count+=1

    choice = int(input("\n>"))
    while (choice not in range (0, count)):
        choice = int(input("Please insert a valid option\n>"))
    
    savefile=savelist[choice]
    setsavefiletoload(savefile)
        
    subprocess.call(GAME_PATH, stdin=None, stdout=None, stderr=None, shell=False)
    saveslot(savefile)
    print(savefile.split("\\")[-1]+" updated!\nSee you next time!\n")

def create_newsavefile():
    newsavefile=""
    fileslist=glob.glob(SLOT_PATH+"\\*.es3")
    if len(fileslist)==0 or not os.path.isfile(SLOT_PATH+"\\Slot1.es3"):
        newsavefile=SLOT_PATH+"\\Slot1.es3"
        shutil.copy(SLOT_PATH+"\\new.save", newsavefile)
        print ("The new save file\n"+newsavefile+"\nhas been created.")
    else:
        for file in fileslist:
            slotnumber=int(file.split("Slot")[-1].split(".es3")[0])
            newsavefile = SLOT_PATH+"\\Slot"+str(slotnumber+1)+".es3"
            if(not os.path.isfile(newsavefile)):
                shutil.copy(SLOT_PATH+"\\new.save", newsavefile)
                print ("The new save file\n"+newsavefile+"\nhas been created.")
                break

    setsavefiletoload(newsavefile)
    subprocess.call(GAME_PATH, stdin=None, stdout=None, stderr=None, shell=False)
    saveslot(newsavefile)
    print(newsavefile.split("\\")[-1]+" updated!\nSee you next time!\n")

def switch_option(option):
    match option:
        case 0 :
            print("See you next time!")
            exit()
        case 1:
            loadexistingsavefile()
        case 2:
            create_newsavefile()
        case 3:
            deletesavefile()
        case _ :
            exit()

def select_option():
    choice = int(input("\n>"))

    while (choice not in range (0, AVAILABLE_OPTIONS)):
        choice = int(input("Please insert a valid option\n>"))

    return choice

def check_first_time():
    if os.path.isdir(SLOT_PATH):
        print ("Welcome back!")
        return
    print("It seems that's your first time running this tool!")
    print("Let me set something first!")
    os.makedirs(SLOT_PATH)
    savefiles = glob.glob(SAVE_PATH+"\\*.es3")
    try:
        latest_savefile = max(savefiles, key= os.path.getmtime)
        shutil.copy(latest_savefile, SLOT_PATH+"\\Slot1.es3")
        print("Your courrent savefile "+ latest_savefile.split("\\")[-1]+" has been saved as Slot1.es3")
        setsavefiletoload(SLOT_PATH+"\\Slot1.es3")
    except:
        print("You have no savefiles to backup right now.")

    shutil.copy("new.save", SLOT_PATH+"\\new.save")
    print("It's all ready! HAVE FUN!\n")
        
def main():
    check_first_time()
    print ("Select an option to start the game:")
    print ("[1] Load a slot")
    print ("[2] Create new save")
    print ("[3] Delete a savefile")
    print ("[0] Exit")
    option = select_option()
    switch_option(option)

if __name__ == "__main__":
    main()