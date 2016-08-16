# Slimelia's Blog Generator (SLIMEBLOGGER)
This is the repository for the source code of my static blog generator I use for my [tilde.town website](http://tilde.town/~slimelia/). The code is a tiny bit messy but I'll pretend that it's just in keeping with tilde.town's brutalist nature!

This generator takes markdown files and generates them into blogposts. It should work as it is, so long as you have the required packages, but I'd *highly* recommend editing the mustache templates in ```tilde.town-slimeblogger/build/templates/``` to customise your blog. Unless you think "Blog Title Here" would be a really deep and meta name for a blog, in which case no changes needed!

I've included a few example markdown documents in ```tilde.town-slimeblogger/build/posts/``` as a demonstration.
Furthermore, ```tilde.town-slimeblogger/public_html/``` only contains ```style.css``` as all other content will be generated when running ```tilde.town-slimeblogger/build/generatePages.py```. The ```style.css``` file is a very basic little starter stylesheet based on the one I use on [my tilde.town blog](http://tilde.town/~slimelia/). Of course, you can completely rework it!

## Markdown formatting

Web blog content is generated from Markdown blog post documents.
All blog posts *MUST* contain a header on the first line.
Headers must follow this format:

`@title Title Goes Here @author author_name_here @date yyyy-mm-dd`

Dates *MUST* be written as yyyy-mm-dd format, using a separator that is **consistent** across **all** markdown blog documents.


## Required packages

Uses the following Python3 libraries:
  * [markdown](https://pythonhosted.org/Markdown/)
  * [pystache](https://github.com/defunkt/pystache)
  * ~~BeautifulSoup4~~ (Currently disabled because it indented the html TOO MUCH) 
