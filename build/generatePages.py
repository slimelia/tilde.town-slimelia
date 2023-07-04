#!/usr/bin/env python3

import os
import markdown
import pystache
#import bs4
import blogpostParser

def getBlogpostsFromDir(dirOfPosts):
	blogParser = blogpostParser.blogpostParser()
	blogpostList = []
	
	
	for filename in os.listdir(dirOfPosts):
		if filename[-3:] == ".md":
			blogpostDict = {}
			fileHandler = open(f"{dirOfPosts}/{filename}",'r',encoding='utf-8')
			lineToParse = fileHandler.readline()
			blogpostDict["body"] = markdown.markdown(fileHandler.read())
			fileHandler.close()
		
			blogpostDict['filename'] = filename.replace(".md",".html")
		
			blogpostAttributes = blogParser.splitBlogStringToDict(lineToParse)
			blogpostAttributes["title"] = blogpostAttributes["title"].lower()
			blogpostDict.update(blogpostAttributes)
			
			blogpostList.append(blogpostDict)
	
	blogpostList.sort(key=lambda postInList: postInList['date'],reverse=True)
	
	return blogpostList
	
def generateBlogpostObj(blogpostTemplateLocation,blogpost):
	posts = []
	content = {}
	
	fileHandler = open(blogpostTemplateLocation,"r")
	blogpostTemplate = fileHandler.read()
	fileHandler.close()
	
	generatedBlogpost = pystache.render(blogpostTemplate,blogpost)
	blogpostObj = {"post":generatedBlogpost}
	
	return blogpostObj
	
def generateBlogPages(dirToWriteTo,blogpostList,templates):
	POST_TEMPLATE = templates[0]
	SITE_TEMPLATE = templates[1]
	
	for blogpostObj in blogpostList:
		blogpost = generateBlogpostObj(POST_TEMPLATE,blogpostObj)
		siteContent = {"content":[blogpost]}
		siteHtml = generateSite(SITE_TEMPLATE,siteContent)
#		parsedSiteHtml = bs4.BeautifulSoup(siteHtml, 'html.parser')
		
		fileHandler = open(f"{dirToWriteTo}/{blogpostObj['filename']}","w")
#		fileHandler.write(parsedSiteHtml.prettify())
		fileHandler.write(siteHtml)
		fileHandler.close()
		
def generateSite(siteTemplateLocation,content):
	fileHandler = open(siteTemplateLocation,"r")
	siteTemplate = fileHandler.read()
	fileHandler.close()
	
	generatedSite = pystache.render(siteTemplate,content)
	
	return generatedSite
	
if __name__ == "__main__":
	postDir = "posts"
	dirForPages = "../public_html/pages"
	postTemplate = "templates/blogpost.mustache"
	siteTemplate = "templates/site.mustache"
	templates = [postTemplate,siteTemplate]
	
	postList = getBlogpostsFromDir(postDir)
	
	generateBlogPages(dirForPages,postList,templates)
	
	index_content = {"content":[]}
	for post in postList:
		index_content["content"].append(generateBlogpostObj(postTemplate,post))
		
	siteHtml = generateSite(siteTemplate,index_content)
#	parsedSiteHtml = bs4.BeautifulSoup(siteHtml, 'html.parser')
	
	index_html = open('../public_html/index.html',"w")
#	index_html.write(parsedSiteHtml.prettify())
	index_html.write(siteHtml)
	index_html.close()
	
	
	
	
