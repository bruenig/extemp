from ExtempFiles.update import MainUpdate

def update():
  paper = "straitstimes"
  feeds = ("http://www.straitstimes.com/STI/STIFILES/rss/break_world.xml",
           "http://www.straitstimes.com/STI/STIFILES/rss/break_money.xml",
           "http://www.straitstimes.com/STI/STIFILES/rss/break_sea.xml")

  #Get links and titles from parsing
  updatepaper = MainUpdate()
  updatepaper.parse(paper, feeds)

  if len(updatepaper.links) == 0:
    print("No new articles found.")
    return 0

  #Do allaffrica specific stuff to the links
  beginurl = "http://www.straitstimes.com/print"
  actualurls = []
  for link in updatepaper.links:
    splitlink = link.split("/")
    actualurl = beginurl + "/" + splitlink[-4] + "/" + splitlink[-3] + "/" + splitlink[-2] + "/" + splitlink[-1]
    actualurls.append(actualurl)

  #Download the modified links
  updatepaper.download(paper, actualurls, updatepaper.titles)

  #Insert the modified links into the DB
  updatepaper.insert(paper, updatepaper.outfiles, updatepaper.outtitles)
