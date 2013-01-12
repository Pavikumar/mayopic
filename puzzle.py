import json
from json import loads
import array
import urllib
import pprint
import random
from pprint import pprint
import os
from random import choice
import imageProcess

class puzzle :
	accessToken = "AAACEdEose0cBAAgr45YojUzmZAZBPqf2RASWxW5L11ASI48LUVVAiTAGk2x3InCxTViox2MwCPresPT6ZBZBcTT1PcePIMvod3MMeYQsfgZDZD"

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
			
	def getInfo(self) :
		url = self.makeURL("me?fields=friends.uid("+self.id+").fields(username,name,birthday,relationship_status)")
		rawdata = urllib.urlopen(url)
		friendraw = rawdata.read()
		#print url
		#print friendraw
		friendInfo = json.loads(friendraw)
		friend = friendInfo['friends']['data'][0]
		self.hints = {}
		if "birthday" in friend :
			self.hints['birthday'] = self.birthday = friend['birthday']
		self.name = friend['name']
		if "relationship_status" in friend :
			self.hints['relationship_status'] = self.relationship_status = friend['relationship_status']
		#pprint(self.hints)
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
			self.ip = imageProcess.imageProcess()
			self.ip.fileName = imgFileName
			self.ip.pixelate()
				
		return imgFileName

	def unPixelate(self) :
		self.ip.incrementSize(5)
		self.ip.pixelate()
    
	def getTaggedPhoto(self):
		url = self.makeURL("me?fields=friends.uid("+self.id+").fields(photos.fields(tags,id))")
		request = urllib.urlopen(url)
		
		response = json.loads(request.read())
		listOfPhotos = response['friends']['data'][0]['photos']['data']
		
		for photo in listOfPhotos :
			if 'tags' not in photo:
				continue
			for tag in photo['tags']['data'] :
				if tag['id'] == self.id :
					photoId = photo['id']
					tagXCoor = tag['x'] 		# x coordinate of tag
					tagYCoor = tag['y']
					imgFileName = self.id+"img.jpg"
					return [urllib.urlretrieve(url, imgFileName), tagXCoor, tagYCoor]
	
	def showHint(self) :
		try :
			self.info
		except AttributeError :
			self.getInfo()
		
		hintKey = random.choice(self.hints.keys())

		hint = "Your friend's " + hintKey + " is " + self.hints[hintKey]

		return hint

p = puzzle()
p.getTaggedPhoto()
