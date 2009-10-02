from ExtempFiles.update import MainUpdate

def update():
  paper = "omahaworldherald"
  feeds = ("http://www.omaha.com/apps/pbcs.dll/section?category=rss&c=news03&mime=xml",
           "http://www.omaha.com/apps/pbcs.dll/section?category=rss&c=money01&mime=xml")

  #Get links and titles from parsing
  updatepaper = MainUpdate()
  updatepaper.parse(paper, feeds)

  if len(updatepaper.links) == 0:
    print("No new articles found.")
    return 0

  #pintable
  actualurls = []
  beginurl="http://www.omaha.com/apps/pbcs.dll/article?AID="
  for link in updatepaper.links:
    splitlink = link.split("/")
    actualurl = beginurl + "/" + splitlink[-3] + "/" + splitlink[-2] + "/" + splitlink[-1] + "&template=printart"
    actualurls.append(actualurl)

  #Download the links
  updatepaper.download(paper, actualurls, updatepaper.titles)

  if len(updatepaper.outfiles) == 0:
    return 0

  #Strip some bad stuff out of the downloaded files
  insertfiles = []
  for file in updatepaper.outfiles:
    insertfiles.append(file.replace('window.print()', ""))

  #Insert the modified links into the DB
  updatepaper.insert(paper, insertfiles, updatepaper.outtitles)
