#!/usr/bin/python
import urllib2, re, json, base64, getpass

print "";
print " GitHubHistorian v0.1 "
print "----------------------"

def getJSON( url ):
  request = urllib2.Request(url)
  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  #With this authentication we can have 5000 GitHub-API-requests per hour.
  request.add_header("Authorization", "Basic %s" % base64string)
  return json.loads(urllib2.urlopen(request).read())

#Settings
useStoredSettings = raw_input("Type 'yes' if you want to use the stored settings:")
if(useStoredSettings=="yes" or useStoredSettings=="y"):
  repo = "ToxicTodo"
  username = "aerobless"
else:
  repo = raw_input("Which repository (name):")
  username = raw_input("Your GitHub username:")

password = getpass.getpass("Your GitHub password: ")

#Get Repo Sha Id
repo_information_json = getJSON('https://api.github.com/repos/'+username+'/'+repo+'/branches')
repo_sha = repo_information_json[0]['commit']['sha']

print "Your SHA-ID: "+repo_sha

#We get one commit, re-commit it in our history repo
#and then get the next commit based on it's parent-sha
repo_commits_json = getJSON('https://api.github.com/repos/'+username+'/'+repo+'/commits/'+repo_sha)

list = []
for k, v in repo_commits_json.iteritems():
  if v > 6:
    list.append(k)
print list

#print repo_commits_json
