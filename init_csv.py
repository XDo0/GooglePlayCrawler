import sys
import csv

def main():
    with open("apps_info.csv", "w", encoding="utf8",newline="") as csvfile:
        file = csv.writer(csvfile)
        file.writerow(
            ['App Title', 'Creator', 'Size', 'Downloads', 'Last Update', 'App ID',
             'Version Code', 'Rating','Description'])
        csvfile.close()




if __name__=="__main__":
    main()

