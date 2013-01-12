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
	
	def __init__(self, token, userId = None) :
		self.accessToken = token
		if userId == None :
			url = self.makeURL("me?fields=friends.fields(id,username)")
			urlData = urllib.urlopen(url)
			data = urlData.read()
			friends = json.loads(data)
			print friends
			listOfFriends = friends['friends']['data']

			amountOfFriends = len(listOfFriends)
			randomFrindNumber = random.randint(1, amountOfFriends)
			randFriend = listOfFriends[randomFrindNumber]
			userId = randFriend['id']
			userName = randFriend['username']
		else:
			url = self.makeURL("me?fields=friends.uid("+userId+").fields(username)")
			urlData = urllib.urlopen(url)
			data = urlData.read()
			friend = json.loads(data)
			userName = friend['friends']['data'][0]['username']
			
		self.id = userId
		self.username = userName
			
	def getInfo(self) :
		url = self.makeURL("me?fields=friends.uid("+self.id+").fields(username,name,birthday,relationship_status,location,hometown)")
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
		if "location" in friend :
			self.hints['location'] = self.location = friend['location']['name']
		if "hometown" in friend :
			self.hints['hometown'] = self.hometown = friend['hometown']['name']
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
	
	def showHint(self, hintsUsed = 0) :
		try :
			self.hints
		except AttributeError :
			self.getInfo()

		if len(self.hints) <= hintsUsed :
			return "There are no more hints available"

		hints=[]
		for hintKey in self.hints :
			hint = "Your friend's " + hintKey + " is " + self.hints[hintKey]
			hints.append(hint)

		return hints[hintsUsed]
