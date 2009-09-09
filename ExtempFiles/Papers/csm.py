from ExtempFiles.update import MainUpdate

def update():
  paper = "csm"
  feeds = ("http://www.csmonitor.com/rss/top.rss",
           "http://rss.csmonitor.com/feeds/usa",
           "http://rss.csmonitor.com/feeds/world")

  #Get links and titles from parsing
  updatepaper = MainUpdate()
  updatepaper.parse(paper, feeds)

  if len(updatepaper.links) == 0:
    print("No new articles found.")
    return 0

  actualurls = []
  dlext=".htm?print=true"
  for link in updatepaper.links:
    splitlink = link.split(".html")
    actualurls.append(splitlink[0] + dlext)

  #Download the links
  updatepaper.download(paper, actualurls, updatepaper.titles)

  if len(updatepaper.outfiles) == 0:
    return 0

  #Format outputted files
  insertfiles = []
  for file in updatepaper.outfiles:
    readfile = file.split("\n")
    insertfile = ""

    for line in readfile:
      if not "window.print()" in line:
        insertfile = insertfile + "\n" + line
        
    insertfiles.append(insertfile)

  #Insert the modified links into the DB
  updatepaper.insert(paper, insertfiles, updatepaper.outtitles)

