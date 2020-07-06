import sys
import csv

def main():
    with open("apps_info.csv", "w", encoding="utf8",newline="") as csvfile:
        file = csv.writer(csvfile)
        file.writerow(
            ['APP ID','CATEGORY','VERSION','DESCRIPTION','DEVELOPER','INSTALLS','REVIEWS','SCORE','SIZE','TITLE'])
        csvfile.close()




if __name__=="__main__":
    main()

