import play_scraper
import os


KEYWORD="security"
NUM=3 #the numbers of apps,there are usually 50 results

def get_app_pname_list(keyword=KEYWORD,num=NUM):
    pname_list=[]
    i=1
    for app in play_scraper.search(keyword):
        if i<=num:
            pname_list.append(app.get('app_id'))
            i+=1
        else:
            break
    return pname_list

def main():
    pname_list=get_app_pname_list()
    with open("free_apps.txt", "a", encoding="utf-8") as f:
        for app_id in pname_list:
            f.write(app_id+"\n")
    f.close()


if __name__=='__main__':
    main()


