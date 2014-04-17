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
else:
  print("The local repository is ready for commits..")

#Get Repo Sha Id
repo_information_json = getJSON('https://api.github.com/repos/'+username+'/'+cRep+'/branches')
repo_sha = repo_information_json[0]['commit']['sha']

print "Your SHA-ID: "+repo_sha

#We get one commit, re-commit it in our history repo
#and then get the next commit based on it's parent-sha
repo_commits_json = getJSON('https://api.github.com/repos/'+username+'/'+cRep+'/commits/'+repo_sha)

list = []
for k, v in repo_commits_json.iteritems():
  if v > 6:
    list.append(k)
print list

print repo_commits_json["commit"]["author"]["name"]
