#!/usr/bin/python
#Imports:
import urllib2, re
import json
import base64

print "";
print " GitHubHistorian v0.1 "
print "----------------------"

#Settings
repo = "ToxicTodo"
username = "aerobless"
password = raw_input("Enter your password: ")

def getJSON( url ):
  request = urllib2.Request(url)
  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  request.add_header("Authorization", "Basic %s" % base64string)
  return json.loads(urllib2.urlopen(request).read())

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
