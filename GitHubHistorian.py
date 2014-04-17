#!/usr/bin/python
import urllib, urllib2, re, json, base64, getpass, sys, os
from subprocess import call

#Program Settings (feel free to change to your liking):
username = "aerobless"                #Your GitHub username
cRep = "ToxicTodo"                    #The commits you want to save before deleting the repo.
hRep = "HistoricCommitData"           #The repo where your historic commits will go
hRepPath = "/Users/theowinter/git/"   #The path to your git folder (where you keep most of your repos)

#Functions:
def getJSON( url ):
  request = urllib2.Request(url)
  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  #With this authentication we can have 5000 GitHub-API-requests per hour.
  request.add_header("Authorization", "Basic %s" % base64string)
  return json.loads(urllib2.urlopen(request).read())

#Main Program:
print ""
print " GitHub Historian v0.2 "
print "-----------------------"
hRepPath = hRepPath+hRep #Appending the repoName

useStoredSettings = raw_input("Type 'yes' if you want to enter custom settings:")
if(useStoredSettings=="yes" or useStoredSettings=="y"):
  cRep = raw_input("Which repository (name):")
  username = raw_input("Your GitHub username:")
password = getpass.getpass("Your GitHub password: ")

#Check if the hRep exists
try:
  hRepData = getJSON('https://api.github.com/repos/'+username+'/'+hRep+'/branches')
except urllib2.HTTPError:
  print ""
  print "INFORMATION:"
  print "GitHubHistorian was unable to detect your historic repository named: "+hRep
  print "Please login to github.com and create a new repository with that name and be sure to initalize it!"
  print "If you already have a repo with a differnet name, you can change the repository name in the settings."
  print ""
  sys.exit()

#Go to local Repo
if not os.path.exists(hRepPath):
  createFolder = raw_input("Your local repo-folder at '"+hRepPath+"' doesn't exist, would you like to create it? yes/no")
  if(createFolder == "yes" or createFolder == "y"):
    os.makedirs(hRepPath)
  else:
    print("You can change the location of the repo-folder in the settings if you wish. Aborting program.")
    sys.exit()
else:
  os.chdir(hRepPath)

#Check git initialisation
gitFolderStatus = call(["git","status"])
if(gitFolderStatus==128):
  print("Initializing the local repository..")
  call(["git","init"])
  call(["touch","commit.history"])
  call(["git","add","commit.history"])
  historyFile = open('commit.history', 'w')
  historyFile.write("1")
  historyFile.close()
else:
  print("The local repository is ready for commits..")

#Get the SHA-ID of the latest commit !! TODO: WHAT HAPPENS WHEN WE HAVE MORE THEN ONE BRANCH !!
repo_information_json = getJSON('https://api.github.com/repos/'+username+'/'+cRep+'/branches')
lastCommitSHA = repo_information_json[0]['commit']['sha']

#We get the latest commit and re-commit it to our history repo
currentCommit = getJSON('https://api.github.com/repos/'+username+'/'+cRep+'/commits/'+lastCommitSHA)

#Current Commit Data (what we need to setup the commit in the history repo)
author_name   = currentCommit["commit"]["author"]["name"]
author_email  = currentCommit["commit"]["author"]["email"]
author_date   = currentCommit["commit"]["author"]["date"]
message       = currentCommit["commit"]["message"]
nextSHA       = currentCommit["parents"][0]["sha"]

#Change a file (so we can actually commit something)
try:
  historyFile = open('commit.history', 'r')
  newNumber = str(int(historyFile.readline())+1)
  historyFile.close()
  historyFile = open('commit.history', 'w')
  historyFile.write(newNumber)
  historyFile.close()
except IOError:
  print("The commit.history file does not exist. Did you delete it? - Creating a new commit.history now.")
  historyFile = open('commit.history', 'w')
  historyFile.write("1")
  historyFile.close()

#Build a commit
call(["git","commit","--date",author_date,"-m","'"+message+"'","--author="+author_name+" <"+author_email+">"])
