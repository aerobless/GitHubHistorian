#!/usr/bin/python
import urllib, urllib2, re, json, base64, getpass, sys
from subprocess import call

#Program Settings (feel free to change to your liking):
username = "aerobless"              #Your GitHub username
currentRepo = "ToxicTodo"           #The commits you want to save before deleting the repo.
historicRepo = "HistoricCommitData" #The repo where your historic commits will go
historicRepoLocalPath = "/Users/theowinter/git/"+historicRepo

#Functions:
def getJSON( url ):
  request = urllib2.Request(url)
  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  #With this authentication we can have 5000 GitHub-API-requests per hour.
  request.add_header("Authorization", "Basic %s" % base64string)
  return json.loads(urllib2.urlopen(request).read())

def createHistoricRepository():
  #call(["mkdir", historicRepo])
  #call(["cd", historicRepo])
  #call(["git", "init"])
  print "done"

#Main Program:
print ""
print " GitHubHistorian v0.1 "
print "----------------------"

useStoredSettings = raw_input("Type 'yes' if you want to enter custom settings:")
if(useStoredSettings=="yes" or useStoredSettings=="y"):
  currentRepo = raw_input("Which repository (name):")
  username = raw_input("Your GitHub username:")
password = getpass.getpass("Your GitHub password: ")

#Check if the HistoricRepo exists
try:
  historicRepoData = getJSON('https://api.github.com/repos/'+username+'/'+historicRepo+'/branches')
except urllib2.HTTPError:
  print ""
  print "INFORMATION:"
  print "GitHubHistorian was unable to detect your historic repository named: "+historicRepo
  print "Please login to github.com and create a new repository with that name and be sure to initalize it!"
  print "If you already have a repo with a differnet name, you can change the repository name in the settings."
  print ""
  sys.exit()

#Get Repo Sha Id
repo_information_json = getJSON('https://api.github.com/repos/'+username+'/'+currentRepo+'/branches')
repo_sha = repo_information_json[0]['commit']['sha']

print "Your SHA-ID: "+repo_sha

#We get one commit, re-commit it in our history repo
#and then get the next commit based on it's parent-sha
repo_commits_json = getJSON('https://api.github.com/repos/'+username+'/'+currentRepo+'/commits/'+repo_sha)

list = []
for k, v in repo_commits_json.iteritems():
  if v > 6:
    list.append(k)
print list

print repo_commits_json["commit"]["author"]["name"]

#Run Shell command
call(["ls", "-l"])

#Create repo test
createHistoricRepository()
