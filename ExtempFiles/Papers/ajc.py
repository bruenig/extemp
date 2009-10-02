from ExtempFiles.update import MainUpdate

def update():
  paper = "ajc"
  feeds = ("http://www.ajc.com/section-rss.do?source=nation-world",
           "http://www.ajc.com/genericList-rss.do?source=94547")

  #Get links and titles from parsing
  updatepaper = MainUpdate()
  updatepaper.parse(paper, feeds)

  if len(updatepaper.links) == 0:
    print("No new articles found.")
    return 0

  #Do allaffrica specific stuff to the links
  actualurls = []
  for link in updatepaper.links:
    actualurl = link.split("?")[0] + "?printArticle=y"
    actualurls.append(actualurl)

  #Download the modified links
  updatepaper.download(paper, actualurls, updatepaper.titles)

  #Insert the modified links into the DB
  updatepaper.insert(paper, updatepaper.outfiles, updatepaper.outtitles)
