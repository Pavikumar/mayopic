import urllib
import Image

#saves the profile image of someone given their facebookname/id thing as img.jpg in the current directory
def getProfilePicture( username ) :
    accesstoken = "AAACEdEose0cBAH1fGZBRpC1jZBZC4XbebcXwFf7oBS646PTR2WK9VStRsiZBPf612KibMldmdldT9xxVivWeqdr01pN94HvEqIZA6CXeWMwZDZD"
    url = "https://graph.facebook.com/"+username+"/picture?width=800&height=800"

    urllib.urlretrieve(url, "img.jpg")

