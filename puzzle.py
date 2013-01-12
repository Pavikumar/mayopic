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

	def makeURL(self, call)	:
		url = "https://graph.facebook.com/" + call + "&access_token="+self.accessToken
		return url
	
	def __init__(self, token) :
		self.accessToken = token
		url = self.makeURL("me?fields=friends.fields(id,username)")
		urlData = urllib.urlopen(url)
		data = urlData.read()
		friends = json.loads(data)
		print friends
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
		url = "https://graph.facebook.com/"+self.username+"/picture?width=400&height=400"
		savingToDirectory = "/srv/www/davidguo.ca/public_html/hackathon2013/hackathon2013/core/images/"		
		imgFileName = self.id+"img.jpg"
		fileExist = False;
		
		for files in os.listdir(savingToDirectory):
			if files == imgFileName and files.endswith(".jpg"):
				fileExist = True
				break
		if fileExist == False :
			urllib.urlretrieve(url, savingToDirectory+imgFileName)
			self.ip = imageProcess.imageProcess()
			self.ip.fileName = savingToDirectory+imgFileName
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
					url = self.makeURL(photoId)
					img = Image()
					imgFileName = self.id+"img.jpg"
					urllib.urlretrieve(url, imgFileName)
					self.ip = imageProcess.imageProcess()
					self.ip.fileName = imgFileName
					img
					return imgFileName
	
	def showHint(self) :
		try :
			self.info
		except AttributeError :
			self.getInfo()
		
		hintKey = random.choice(self.hints.keys())

		hint = "Your friend's " + hintKey + " is " + self.hints[hintKey]

		return hint
