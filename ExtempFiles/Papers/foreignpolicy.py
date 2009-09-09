from ExtempFiles.update import MainUpdate

def update():
  paper = "foreignpolicy"
  feeds = ("http://www.foreignpolicy.com/issue/featured_content.php",
           "http://www.foreignpolicy.com/node/feed",
           "http://www.foreignpolicy.com/taxonomy/term/655/0/feed")

  #Get links and titles from parsing
  updatepaper = MainUpdate()
  updatepaper.parse(paper, feeds)

  if len(updatepaper.links) == 0:
    print("No new articles found.")
    return 0

  #Scrap articles for printable link
  updatepaper.scrape(paper, updatepaper.links, updatepaper.titles)

  if len(updatepaper.scrapefiles) == 0:
    print("No new articles found.")
    return 0

  #Get printable urls
  actualurls = []
  actualtitles = []
  total = len(updatepaper.scrapefiles)
  for num, file in enumerate(updatepaper.scrapefiles):
    for line in file:
      if '>PRINT' in line:
        actualurls.append(line.split('"')[1])
        actualtitles.append(updatepaper.scrapetitles[num])
        break

  #Download the scraped links
  updatepaper.download(paper, actualurls, actualtitles)

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
