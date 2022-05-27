'''
DEVELOPER: Jack Utter
COLLABORATORS: NA
DATE: 04/24/2022
'''

"""A database for a service based company.

Manages the txt files detailing the client list, the visits to clients for service, and the times those services began and finished.
"""

##########################################
# IMPORTS:
#   <list modules needed for program and their purpose>
##########################################
#none


##########################################
# GLOBAL VARIABLES:
##########################################
CLIENTDATABASE = "ClientDatabase.txt"
TIMELOG = "timeLog.txt"
VISITS = "Visits.txt"

##########################################
# CLASSES:
##########################################

class Client :
  def __init__(self, name = "", address = "", phoneNumber = "") :
    self.name = name
    self.address = address
    self.phoneNumber = phoneNumber
    
  def setName(self, name) :
    self.name = name
  def getName(self) :
    return self.name
  def setAddress(self, address) :
    self.address = address
  def getAddress(self) :
    return self.address
  def setPhoneNumber(self, phoneNumber) :
    self.phoneNumber = phoneNumber
  def getPhoneNumber(self) :
    return self.phoneNumber
    
  def __str__(self) :
    return f"{self.address}; {self.phoneNumber}"

##########################################
# FUNCTIONS:
##########################################
    
#######################################################################  
                  #########Encryption##########  
#######################################################################  
    
def encrypt(content : str) :
#encrypt sensitive data before being stored in a file
  pass
def decrypt(content : str) :
  #decrypt sensitive data after being read from a file
  pass

#######################################################################  
      #####Saving and loading databases (dictionaries)######### 
                  ########to and from files#####  
#######################################################################  
  
def writeToFile(fileName : str, content) :
  #writes data to external files to store information
  file = open(fileName, "w")
  file.write(content)
  file.close
  return True

def writeDatabaseToFile(fileName : str, db : {}) :
  #prepares a database to be written to a txt file
  dbString = ""
  for obj in db :
    dbString += f"{obj}; {(db.get(obj))} \n"
  writeToFile(fileName, dbString)
  return True
  
def readFromFile(fileName : str) :
  #read file and return the content
  try:
    file = open(fileName, "r")
    fileContent = file.readlines()
    file.close
    return fileContent
  except(IOError):
    print(f"Error reading file \"{fileName}\".")
    
def readDBFromFile(fileName :str) :
  #returns a dictionary from a file
  db = {}
  contents = readFromFile(fileName)
  for line in contents :
    if line == "" :  #skip empty lines
      continue 
    sd = line.split(';')
    
    if ("(" in line) : #timeLogDB - a dictionary of a str key and a 2tuple value
      listSplit = (sd[1].strip()).split(',')
      db[sd[0]] = (listSplit[0].strip("(").strip("'"), listSplit[1].strip("(").strip(")").strip().strip("'"))
    elif len(sd) == 2 :  
      #visitsDB - a dictionary of a str key and a list value
      listSplit = (sd[1].strip()).split(',')
      db[sd[0]] = []
      for entry in listSplit :
        strippedEntry = entry.strip("[").strip("]").strip().strip("'")
        if strippedEntry != "" :
          db[sd[0]].append(strippedEntry)
    else:  #clientDB - a dictionary of a str key and a Client obj value
      db[sd[0]] = Client(sd[0].strip(), sd[1].strip(), sd[2].strip())
      
  return db
#######################################################################  
                      ######Database UI######  
#######################################################################  
  
def addClient(name, address, phoneNumber) :
  #Add a client to the CLIENTDATABASE
  clientDB = readDBFromFile(CLIENTDATABASE)
  visitDB = readDBFromFile(VISITS)
  clientDB[name] = Client(name, address, phoneNumber)
  visitDB[name] = []
  writeDatabaseToFile(CLIENTDATABASE, clientDB)
  writeDatabaseToFile(VISITS, visitDB)
  
def addClientPrompts() :
  #Add a client to the CLIENTDATABASE via prompts
  clientDB = readDBFromFile(CLIENTDATABASE)
  while True :
    name = input("Enter client name: ")
    if name in clientDB :
      #No duplicates in the CLIENTDATABASE
      print(f"{name} is already a client.")
      continue
    break
  address = input("Enter client address: ")
  phoneNumber = input("Enter client phone number(000-000-0000) : ")
  addClient(name, address, phoneNumber)

def addServiceEvent(name, date, start, finish) :
  #log a service event to the TIMELOG and VISITS logs
  timeDB = readDBFromFile(TIMELOG)
  visitDB = readDBFromFile(VISITS)

  visitDB[name].append(date)
  timeDB[(name + ", " + date)] = (start, finish)

  writeDatabaseToFile(TIMELOG, timeDB)
  writeDatabaseToFile(VISITS, visitDB)

def addServiceEventPrompts() :
  #log a service event to the TIMELOG and VISITS logs via prompts
  clientDB = readDBFromFile(CLIENTDATABASE)
  visitDB = readDBFromFile(VISITS)
  timeDB = readDBFromFile(TIMELOG)
  name = input("Enter client name: ")
  if name not in clientDB :
    print(f"\"{name}\" not found in client Database")
    return
  date = input("Enter date of service(MO/DA/YEAR) : ")
  if date in visitDB[name] :
    print(f"{date} has already been logged for {name}.")
    return
  startTime = input("Enter time service started(00:00) : ")
  finishTime = input("Enter time service finished(00:00) : ")
  addServiceEvent(name, date, startTime, finishTime)
  
def printClientList() :
  #prints a reasonably formated client list from the CLIENTDATABASE
  clientDB = readDBFromFile(CLIENTDATABASE)
  for client in clientDB :
    print(f"{client:18} {str(clientDB[client])}")
def printTimeLog() :
  #prints a reasonably formated TIMELOG
  timeLogDB = readDBFromFile(TIMELOG)
  for entry in timeLogDB :
    splitEntry = entry.split(',')
    print(f"{splitEntry[0].strip():18} {splitEntry[1].strip():12} {timeLogDB[entry]}")
def printVisitsLog() :
  #prints a reasonably formated VISITS
  visitsDB = readDBFromFile(VISITS)
  for entry in visitsDB :
    print(f"{entry:18} {visitsDB[entry]}")

  
##########################################
# MAIN PROGRAM:
##########################################
def main():
  print("The Happy Brothers Lawn Mowing Business Client and Service Log\n\n")
  while True :
    menuMessage = "\nActions :\n\tPrint Client List\n\tPrint Time Log\n\tPrint Visits Log\n\tAdd Client\n\tLog Service\n\tQuit\n"
    userMenuSelection = input(menuMessage).upper()
    if userMenuSelection == "Print Client List".upper() :
      printClientList()
    elif userMenuSelection == "Print Time Log".upper() :
      printTimeLog()
    elif userMenuSelection == "Print Visits Log".upper() :
      printVisitsLog()
    elif userMenuSelection == "Add Client".upper() :
      addClientPrompts()
    elif userMenuSelection == "Log Service".upper() :
      addServiceEventPrompts()
    elif userMenuSelection == "quit".upper() :
      break
    else :
      print("huh?")  
    
  
main()
