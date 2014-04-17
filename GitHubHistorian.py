#!/usr/bin/python
#Imports:
import urllib2, re
import json

print "GitHubHistorian v0.1"
repo = "ParProg"
username = "aerobless"

#Get Repo Sha Id
response = urllib2.urlopen('https://api.github.com/repos/'+username+'/'+repo+'/branches')
data = json.loads(response.read())

print "Your SHA-ID: "+data[0]['commit']['sha']


#print(html)
#curl https://api.github.com/repos/aerobless/ParProg/commits?per_page=100&sha=1555807af6ccd917049c461cc9f137e05fdd8ed8
