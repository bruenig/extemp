from ExtempFiles.update import MainUpdate

def update():
  paper = "feer"
  feeds = ("http://www.feer.com/rss?cat=politics",
           "http://www.feer.com/rss?cat=international-relations",
           "http://www.feer.com/rss?cat=economics")

  #Get links and titles from parsing
  updatepaper = MainUpdate()
  updatepaper.parse(paper, feeds)

  if len(updatepaper.links) == 0:
    print("No new articles found.")
    return 0

  #Download the links
  updatepaper.download(paper, updatepaper.links, updatepaper.titles)

  if len(updatepaper.outfiles) == 0:
    return 0

  #Format outputted files
  insertfiles = []
  for file in updatepaper.outfiles:
    readfile = file.split("\n")
    insertfile = "<b>Far Eastern Economic Review</b>"

    dowrite = 0
    for line in readfile:
      if dowrite == 1:
        if '<div class="content_box">' in line:
          break
        else:
          insertfile = insertfile + "\n" + line
      elif "<!-- Some content EG article -->"  in line:
        dowrite = 1
        
    insertfiles.append(insertfile)

  #Insert the modified links into the DB
  updatepaper.insert(paper, insertfiles, updatepaper.outtitles)

