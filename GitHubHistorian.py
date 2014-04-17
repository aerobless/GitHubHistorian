#!/usr/bin/python
#Imports:
import urllib2, re
import json

print "";
print " GitHubHistorian v0.1 "
print "----------------------"

#Settings
repo = "ToxicTodo"
username = "aerobless"

#Get Repo Sha Id
repo_information_str = urllib2.urlopen('https://api.github.com/repos/'+username+'/'+repo+'/branches')
repo_information_json = json.loads(repo_information_str.read())
repo_sha = repo_information_json[0]['commit']['sha']

print "Your SHA-ID: "+repo_sha

#Get commits
repo_commits_str = urllib2.urlopen('https://api.github.com/repos/'+username+'/'+repo+'/commits?per_page=100&sha='+repo_sha)
repo_commits_json = json.loads(repo_commits_str.read())
print repo_commits_json
