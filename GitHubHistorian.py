#!/usr/bin/python
import urllib2, re, json, base64, getpass
from subprocess import call

#Program Settings (feel free to change to your liking):
currentRepo = "ToxicTodo"         #The commits you want to save before deleting the repo.
historicRepo = "GitHubHistory"  #The repo where your historic commits will go
username = "aerobless"            #Your GitHub username

#Functions:
def getJSON( url ):
  request = urllib2.Request(url)
  print url
  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  #With this authentication we can have 5000 GitHub-API-requests per hour.
  request.add_header("Authorization", "Basic %s" % base64string)
  return json.loads(urllib2.urlopen(request).read())

def createHistoricRepository():
  #call(["mkdir", historicRepo])
  #call(["cd", historicRepo])
  #call(["git", "init"])
  repoDescription = "Repository containing historic commit-data. Generated with GitHubHistorian." #todo add link
  repoBuilder = '{"name":"'+historicRepo+'","description":"'+repoDescription+'"}'
  #getJSON("https://api.github.com/user/repos -d '"+repoBuilder+"'")
  getJSON("https://api.github.com/user/repos -d '{\"name\":\"test\",\"description\":\"my new repo description\"}'")
  #curl -u "aerobless"  https://api.github.com/user/repos -d '{"name":"my-new-repo","description":"my new repo description"}'
  print "done"

#Main Program:
print ""
print " GitHubHistorian v0.1 "
print "----------------------"

useStoredSettings = raw_input("Type 'yes' if you want to enter custom settings:")
if(useStoredSettings=="yes" or useStoredSettings=="y"):
  repo = raw_input("Which repository (name):")
  username = raw_input("Your GitHub username:")

password = getpass.getpass("Your GitHub password: ")

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
