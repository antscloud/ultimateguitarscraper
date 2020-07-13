import requests
import urllib.request
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import argparse
import json
import os 
import sys


def main(args2):

    VALUES=["[Intro]","[Verse]","[Verse 1]","[Verse 2]","[Verse 3]","[Verse 4]","[Pre-Chorus]","[Pre-Chorus 1]","[Pre-Chorus 2]","[Pre-Chorus 3]","[Chorus]","[Chorus 1]","[Chorus 2]","[Chorus 3]","[Bridge]","[Bridge 1]","[Bridge 2]","[Bridge 3]","[Outro]","[Interruption]","[Instrumental]","[Interlude]"]

    CONTENT_DIV=("pre",{"class":"_3zygO"})
    DOUBLE_DIV_CHORDS_LYRICS=("span",{"class":"_2J-ci"})
    SINGLE_DIV_CHORDS_LYRICS=("span",{"class":"_1zlI0"})
    CHORDS_DIV=("span",{"class":"_3bHP1"})
    CHORDS_DIV2=("span",{"class":"_3ffP6"})
    HEADER_DIV_NAME_ARTIST=("header",{"class":"_2Glbj"})
    META_SONG=("div",{"class":"_1H6vh"})


    path=os.getcwd()

    parser=argparse.ArgumentParser()
    parser.add_argument("url", help="url to scrape")
    parser.add_argument("-a","--all_text", help="Scrape content of the tab",action="store_true")
    parser.add_argument("-j","--json", help="Create a json file with multiple infos", action="store_true")
    parser.add_argument("-l","--lyrics", help="Scrape only lyrics", action="store_true")
    parser.add_argument("-c","--chords", help="Scrape only chords", action="store_true")
    parser.add_argument("-p","--pathtochrome", help="Path to chromedriver, In the folder from where the script is executed by default", nargs='?' )
    parser.add_argument("-i","--ignoresave", help="Ignore messages concerning overwriting files", action="store_true")
    parser.add_argument("-f","--folder", help="Create folder",nargs='?')
    args=parser.parse_args(args2)

    ignore=args.ignoresave
    driver=None

    if args.folder is None:
        parser.error("argument -f/--folder: expected one argument. Please specify a folder : '-f test' for instance")

    url=args.url

    if not args.folder:
        foldername=""
    else:
        foldername=args.folder.replace("\\","").replace("/","")+"/"

    if args.folder:
        pathfolder=os.path.join(os.path.dirname(__file__),foldername)
        if os.path.isdir(pathfolder) or os.path.isfile(pathfolder):
            try: 
                raise FileExistsError("Directory already exist")
            except:
                print("Directory already exist.")
        else:
            os.mkdir(pathfolder)

    if args.pathtochrome:
        pathtochromedriver=args.pathtochrome
    else: 
        pathtochromedriver="chromedriver.exe"

    def initialize(url=url,path=pathtochromedriver):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(path,options=options) 
        driver.get(url)
        soup=BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return soup

    def find_lyrics(page):
        """
        Return lyrics in a list
        """
        a=soup.find(*CONTENT_DIV)
        list_of_span_with_text=a.findAll(*DOUBLE_DIV_CHORDS_LYRICS)
        lyrics=[]
        for i in range(len(list_of_span_with_text)):
            lyrics.append(list_of_span_with_text[i].findAll(*SINGLE_DIV_CHORDS_LYRICS))
        
        for i in range(len(lyrics)):
            lyrics[i]=lyrics[i][1].text

        value_to_remove=[]
        for i in range(len(lyrics)):
            if re.search(r"(https|http)|[-]{2,}|[ ]{4,}",str(lyrics[i])):
                value_to_remove.append(lyrics[i])
        lyrics=[e for e in lyrics if e not in value_to_remove]
        return lyrics

    def find_lyrics_str(page):
        """
        Return lyrics in a unique string
        """
        lyrics_list=find_lyrics(page)
        lyrics=""
        for i in range(len(lyrics_list)):
            lyrics+=str(lyrics_list[i].replace("\n",". ").replace("\r",""))
        return lyrics
        

    def find_chords_list(page):
        """
        Return list of all chords in order
        """
        a=page.find(*CONTENT_DIV)
        list_of_span_with_text=a.findAll(*CHORDS_DIV)
        chords=[]
        chords_inter=[]
        for i in range(len(list_of_span_with_text)):
            chords.append(list_of_span_with_text[i])
            
        
        chords_inter.append(clean_chords(chords))
        return chords_inter

    def find_structure(soup):
        """
        find_structure return a tuple (i,j) with i the list  index of the span, and j 
        the list of the value of the bracket 
        for instance ([1,2],["[VERSE]","[CHORUS]"])
        """
        a=soup.find(*CONTENT_DIV)
        all_span=a.findAll("span",recursive=False)

        index_of_span=[]
        value_of_bracket=[]
        for i in range(len(all_span)):
            #find in bracket
            if re.findall(r"\[(.*?)\]",all_span[i].text) != []:
                bracket="["+re.findall(r"\[(.*?)\]",all_span[i].text)[0]+"]"
                if bracket in VALUES:
                    index_of_span.append(i)
                    value_of_bracket.append(all_span[i])

        return index_of_span,value_of_bracket

    def find_chords_list_from_bracket(page):

        index_of_span, _ =find_structure(page)
        a=page.find(*CONTENT_DIV)
        all_span=a.findAll("span",recursive=False)
        chords_inter=[]
        for i in range(len(index_of_span)):
            chords=[]
            if i ==len(index_of_span)-1:
                iterspan=range(index_of_span[i]+1,len(all_span))
            else : 
                iterspan=range(index_of_span[i]+1,index_of_span[i+1])

            for j in iterspan:
                all_chords=all_span[j].findAll(*CHORDS_DIV)
                for k in range(len(all_chords)):
                    chords.append(all_chords[k])

            chords_inter.append(clean_chords(chords))
        return chords_inter

    def clean_chords(chords):
        chords_part=0
        chords_list=0
        chords_str=""
        for k in range(len(chords)):
            chords[k]=chords[k].text.replace("\r","").replace("\n","")
            chords[k]=re.sub(' +', ',',chords[k])
            chords_str += "," + str(chords[k])
        chords_list=chords_str.split(",")
        value_to_remove=[]
        for k in range(len(chords_list)):
            if re.search(r"[ .\[\]\{\}\'\%\|]|^[a-z]|[-]{2,}",str(chords_list[k])):
                value_to_remove.append(chords_list[k])
        chords_part=[e for e in chords_list if (e not in value_to_remove)]
        chords_part=[e for e in chords_part if (e!="")]
        return chords_part


    def save_chords_lyrics(filename,foldername,ignore,values):
        if ignore:
            with open(foldername+filename,"w") as f:
                    for i in range(len(values)):
                        f.write(values[i])
        else:
            if os.path.isfile(foldername+filename):
                loop=True
                while loop:
                    choice=input("File already exist. Do you want to overwrite it ? (Y/N) ")
                    if choice in ["Y",'y'] :
                        with open(foldername+filename,"w") as f:
                            for i in range(len(values)):
                                f.write(values[i])
                        loop=False
                    elif choice in ["N",'n']:
                        print("Execution interrupted.")
                        break 
                    else:
                        print("Please specify a choice : Y or N")
                        pass
            else: 
                with open(foldername+filename,"w") as f:
                    for i in range(len(values)):
                        f.write(values[i])

    def save_all(filename,foldername,ignore,a):
        if ignore:
            with open(foldername+filename,"w") as f:
                        f.write(a.text)
        else:
            if os.path.isfile(foldername+filename):
                loop=True
                while loop:
                    choice=input("File already exist. Do you want to overwrite it ? (Y/N) ")
                    if choice in ["Y",'y'] :
                        with open(foldername+filename,"w") as f:
                            f.write(a.text)
                        loop=False
                    elif choice in ["N",'n']:
                        print("Execution interrupted.")
                        break 
                    else:
                        print("Please specify a choice : Y or N")
                        pass
            else: 
                with open(foldername+filename,"w") as f:
                    f.write(a.text)
    def save_json(filename,foldername,ignore,data):
        if ignore:
            with open(foldername+filename,'w') as f:
                json.dump(data,f)
        else:
                if os.path.isfile(foldername+filename):
                    loop=True
                    while loop:
                        choice=input("File already exist. Do you want to overwrite it ? (Y/N) ")
                        if choice in ["Y",'y'] :
                            with open(foldername+filename,'w') as f:
                                json.dump(data,f)
                            loop=False
                        elif choice in ["N",'n']:
                            print("Execution interrupted.")
                            break 
                        else:
                            print("Please specify a choice : Y or N")
                            pass
                else: 
                    with open(foldername+filename,'w') as f:
                        json.dump(data,f)
    
    soup=initialize(url)

    if args.all_text:
        try:
            a=soup.find(*CONTENT_DIV)

            datasong=soup.find(*HEADER_DIV_NAME_ARTIST)
            filename=datasong.h1.text.replace(" chords","")+"-"+datasong.span.text.replace(" by ","")+"-all"+".txt"

            save_all(filename,foldername,ignore,a)

        except IOError as e:
            print(e)
            print("If you want to create a folder please specify the '-f'")
        except Exception as e:
            print(e)
            print("An error has  occurred. The driver will close. It may be the connection, please check it.")

    if args.lyrics:
        try:

            a=soup.find(*CONTENT_DIV)

            datasong=soup.find(*HEADER_DIV_NAME_ARTIST)
            filename=datasong.h1.text.replace(" chords","")+"-"+datasong.span.text.replace(" by ","")+"-lyrics"+".txt"


            list_of_span_with_text=a.findAll(*DOUBLE_DIV_CHORDS_LYRICS)
            lyrics=[]
            for i in range(len(list_of_span_with_text)):
                lyrics.append(list_of_span_with_text[i].findAll(*SINGLE_DIV_CHORDS_LYRICS))
            
            for i in range(len(lyrics)):
                lyrics[i]=lyrics[i][1].text
            save_chords_lyrics(filename,foldername,ignore,lyrics)
        except IOError as e:
            print(e)
            print("If you want to create a folder please specify the '-f'")
        except Exception as e: 
            print(e)
            print("An error has  occurred. The driver will close. It may be the connection, please check it.")

    if args.chords:
        try:

            a=soup.find(*CONTENT_DIV)

            datasong=soup.find(*HEADER_DIV_NAME_ARTIST)
            filename=datasong.h1.text.replace(" chords","")+"-"+datasong.span.text.replace(" by ","")+"-chords"+".txt"

            list_of_span_with_text=a.findAll(*DOUBLE_DIV_CHORDS_LYRICS)
            chords=[]
            for i in range(len(list_of_span_with_text)):
                chords.append(list_of_span_with_text[i].findAll(*SINGLE_DIV_CHORDS_LYRICS))
            
            for i in range(len(chords)):
                chords[i]=chords[i][0].text.replace("\r","")
                chords[i]=re.sub(' +', ' ',chords[i])
                chords[i]=re.sub("^\s",'',chords[i])
            
            save_chords_lyrics(filename,foldername,ignore,chords)
        except IOError as e:
            print(e)
            print("If you want to create a folder please specify the '-f'")
        except Exception as e:
            print(e)
            print("An error has  occurred. The driver will close. It may be the connection, please check it.")

    if args.json:
        try:
            data={}
            data["structure"]={}

            datasong=soup.find(*HEADER_DIV_NAME_ARTIST)
            data["titlename"]=datasong.h1.text.replace(" chords","")
            data["artistname"]=datasong.span.text.replace(" by ","")
            data["all_lyrics"]=find_lyrics_str(soup)
            data["allchords"]=find_chords_list(soup)
            metasong=soup.find(*META_SONG).findAll("div")
            for i in range(len(metasong)):
                testdata=metasong[i].text 
                if re.search("Key",testdata):
                    data["key"]=testdata.replace("Key: ","")
                if re.search("Tuning",testdata):
                    data["tuning"]=testdata.replace("Tuning: ","").split(' ')

            list_of_chords_by_bracket=find_chords_list_from_bracket(soup)
            _, value_of_bracket=find_structure(soup)

            if len(list_of_chords_by_bracket)==len(value_of_bracket):
                for i in range(len(value_of_bracket)):
                    value_of_bracket[i]=value_of_bracket[i].text.replace("\r\n","")
                    data["structure"][value_of_bracket[i]]=list_of_chords_by_bracket[i]
            else :
                raise ValueError("Number of bracket {} and number of elements of the list of chords {} does not correspond ".format(len(value_of_bracket),len(list_of_chords_by_bracket)))
            
            filename=data["titlename"]+"-"+data["artistname"]+".json"

            save_json(filename,foldername,ignore,data)
        except IOError as e:
            print(e)
            print("If you want to create a folder please specify the '-f'")
        except Exception as e: 
            print(e)
            print("An error has  occurred. The driver will close. It may be the connection, please check it.")
    
    return soup


if __name__ == "__main__":
    print(' '.join(sys.argv[1:]))
    main(sys.argv[1:])