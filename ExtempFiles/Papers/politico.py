from ExtempFiles.update import MainUpdate

def update():
  paper = "politico"
  feeds = ("http://www.politico.com/rss/congress.xml",
           "http://www.politico.com/rss/politics.xml")

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
  for num, file in enumerate(updatepaper.scrapefiles):
    for line in file:
      if 'shr-print' in line:
        actualurls.append(line.split('"')[3])
        actualtitles.append(updatepaper.scrapetitles[num])
        break

  #Download the scraped links
  updatepaper.download(paper, actualurls, actualtitles)

  #Insert the modified links into the DB
  updatepaper.insert(paper, updatepaper.outfiles, updatepaper.outtitles)
