import json
from json import loads
import array
import urllib
import pprint
import random
from pprint import pprint
import os

class puzzle :
	accessToken = "AAAF0HW88pkcBAOknQJOsOgNz8w9AEdWZBdYucMySiYZBmyaLU7U1CtSZA6VvYfS1iCUz5reKsdjfPQ5MWZB7M0GaZCGUsvUrLGkkcU6oVLgZDZD"

	def makeURL(self, call)	:
		url = "https://graph.facebook.com/" + call + "&access_token="+self.accessToken
		return url
	
	def __init__(self) :
		url = self.makeURL("me?fields=friends.fields(id,username)")
		urlData = urllib.urlopen(url)
		data = urlData.read()
		friends = json.loads(data)
		listOfFriends = friends['friends']['data']

		amountOfFriends = len(listOfFriends)
		randomFrindNumber = random.randint(1, amountOfFriends)
		randFriend = listOfFriends[randomFrindNumber]
		self.id = randFriend['id']
		self.username = randFriend['username']
			
	def getinfo(self) :
		url = self.makeURL("me?fields=friends.uid("+self.id+").fields(username,name,birthday,relationship_status)")
		rawdata = urllib.urlopen(url)
		friendraw = rawdata.read()
		friendInfo = json.loads(friendraw)
		friend = friendInfo['friends']['data']
		self.birthday = friendInfo['birthday']
		self.name = friendInfo['Kitna Chan']
		self.relationship_status = friendInfo['In a Relationship']
                #returns a dict containing birthday, id, name, relationsip status, and username
		return friend
	
	def getProfilePicture(self) :
		url = "https://graph.facebook.com/"+self.username+"/picture?width=800&height=800"
		imgFileName = self.id+"img.jpg"
		fileExist = False;
		for files in os.listdir("."):
			if files == imgFileName and files.endswith(".jpg"):
					fileExist = True
					break
		if fileExist == False :
				urllib.urlretrieve(url, imgFileName)
		return imgFileName

	def showHint() :
		print "hello"

p = puzzle()
p.getProfilePicture()

