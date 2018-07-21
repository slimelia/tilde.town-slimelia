#!/usr/bin/env python3

class blogpostParser:
	def splitBlogStringToDict(self,stringToSplit):
		stringToSplit = stringToSplit.replace(" @","@")
		splitStringList = stringToSplit.split("@")[1:]	#Split by @ and disregard first element (empty string)
		
		blogAttributes = {}
		
		for element in splitStringList:
			key,val = element.partition(" ")[0::2] #Split by first ' ' and disregard separator tuple element (result will always be list of 3 indices)
			blogAttributes[key] = val
		return blogAttributes

if __name__ == "__main__":
	exampleString = "@title Example Title @author slimelia @date Today"
	exampleDict = splitBlogStringToDict(exampleString)
	print(exampleDict)
