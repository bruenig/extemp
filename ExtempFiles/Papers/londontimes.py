from ExtempFiles.update import MainUpdate

def update():
  paper = "londontimes"
  feeds = ("http://feeds.timesonline.co.uk/c/32313/f/440158/index.rss",
           "http://feeds.timesonline.co.uk/c/32313/f/440154/index.rss")

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

  #Change links to printable
  beginurl = "http://timesonline.co.uk"
  dlext = "?print=yes"
  actualurls = []
  actualtitles = []
  total = len(updatepaper.scrapefiles)
  for num, file in enumerate(updatepaper.scrapefiles):
    for line in file:
      if "print-comment" in line:
        actualurls.append(beginurl + line.split("'")[1] + dlext)
        actualtitles.append(updatepaper.scrapetitles[num])
        break

  #Download the links
  updatepaper.download(paper, actualurls, updatepaper.titles)

  #Insert the modified links into the DB
  updatepaper.insert(paper, updatepaper.outfiles, updatepaper.outtitles)
