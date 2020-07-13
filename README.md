# ultimateguitarscraper

A command line interface scraper for Ultimate Guitar. Works only with the Chords Tab. 


# How to use :

## Chrome Driver :
In order to use this script, the chromedriver is needed. You can find it [here](https://chromedriver.chromium.org/downloads).

## Download 

You can download the repo : 

    git clone https://github.com/antscloud/ultimateguitarscraper.git

## Use 
As there is only one important file : scrape.py.
You can copy and paster this file where you want it to run.
For an easier use you can just copy paste the chrome driver in the same repository.

    parentfolder
        chromedriver.exe
        scrape.py
            
There are multiple arguments to pass, only one is required : the url. But if no other arguments are precised, the script is quite useless. It will just scrape the page but do nothing with this. 
Here are the availables arguments : 

    usage: scrape.py [-h] [-a] [-j] [-l] [-c] [-p [PATHTOCHROME]] [-i]
                     [-f [FOLDER]]
                     url

    positional arguments:
      url                   url to scrape

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all_text        Scrape content of the tab
      -j, --json            Create a json file with multiple infos
      -l, --lyrics          Scrape only lyrics
      -c, --chords          Scrape only chords
      -p [PATHTOCHROME], --pathtochrome [PATHTOCHROME]
                            Path to chromedriver, In the folder from where the
                            script is executed by default
      -i, --ignoresave      Ignore messages concerning overwriting files
      -f [FOLDER], --folder [FOLDER]
                            Create folder
                            
## Examples : 

    python scrape.py https://tabs.ultimate-guitar.com/tab/ed-sheeran/perfect-chords-1956589 -f test -i -l

This command create a new folder named "test" (if argument not precised then the files will be in your current repo), ignore messages concerning overwriting files, and extrac all the lyrics of the song. 

                            
  #Import and use it 
  
  You can also import it. At this moment, the file is not in pyi yet. 
  
      import scrape
      
      cmd="https://tabs.ultimate-guitar.com/tab/ed-sheeran/perfect-chords-1956589 -f test -i -c -a -l -j"
      scrape.main(cmd.split(" "))
      
This will create 4 files based on the url. A json file and 3 texts files. 
