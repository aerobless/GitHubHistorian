#!/usr/bin/python
import urllib, urllib2, re, json, base64, getpass, sys, os
from subprocess import call

#Program Settings (feel free to change to your liking):
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
print " GitHub Historian v0.3 "
print "-----------------------"

hRep = raw_input("Name of the repository that will contain the Commit-History:")
cRep = raw_input("Name of the repostiory that's about to be archived:")
username = raw_input("Your GitHub username:")
password = getpass.getpass("Your GitHub password: ")

hRepPath = hRepPath+hRep #Appending the repoName

#Check if the hRep exists
try:
  hRepData = getJSON('https://api.github.com/repos/'+username+'/'+hRep+'/branches')
except urllib2.HTTPError:
  print ""
  print "INFORMATION:"
  print "GitHubHistorian was unable to detect your historic repository named: "+hRep
  print "Please login to github.com and create a new repository with that name and be sure to initalize it!"
  print "If you already have a repo with a different name, you can change the repository name in the settings."
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
  call(["git","remote","add","origin","https://"+username+"@github.com/"+username+"/"+hRep+".git"])
  call(["git","pull","origin","master"])
  call(["touch","commit.history"])
  call(["git","add","commit.history"])
  historyFile = open('commit.history', 'w')
  historyFile.write("1")
  historyFile.close()
else:
  print("The local repository is ready for commits..")

#Get the SHA-ID of the latest commit !! TODO: WHAT HAPPENS WHEN WE HAVE MORE THEN ONE BRANCH !!
repo_information_json = getJSON('https://api.github.com/repos/'+username+'/'+cRep+'/branches')
commitSHA = repo_information_json[0]['commit']['sha']

#Download all the commit information into a list
commitList = []
print "Downloading commit-data from GitHub (this may take a while)"
while True:
  currentCommit = getJSON('https://api.github.com/repos/'+username+'/'+cRep+'/commits/'+commitSHA)
  print "Working on commit: "+str(len(commitList))
  currentCommitInfo = []
  currentCommitInfo.append(currentCommit["commit"]["author"]["name"])
  currentCommitInfo.append(currentCommit["commit"]["author"]["email"])
  currentCommitInfo.append(currentCommit["commit"]["author"]["date"])
  currentCommitInfo.append(currentCommit["commit"]["message"])
  commitList.append(currentCommitInfo)
  try:
    commitSHA=currentCommit["parents"][0]["sha"]
  except IndexError:
    break

#Iterate through list to build commits
print("Creating historical commits...")
call(["git","pull","origin","master"])
for element in commitList:
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
  call(["git","commit","--date",element[2],"-am","Archived "+cRep+": '"+element[3]+"'","--author="+element[0]+" <"+element[1]+">"])

#Finally pushing everything to the remote
print ""
print "We're all done! Enter your password to confirm that you want to push the historic data to GitHub!"
call(["git","push","origin","master"])
