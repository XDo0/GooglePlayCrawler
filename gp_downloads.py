# coding:utf-8
# !/usr/bin/python
# -*- coding: utf-8 -*-
# PythonScript.py

'''
Deprecated script
'''

from pprint import pprint
from multiprocessing import Pool

import time
import collections
import os
from gplaycli import gplaycli
import subprocess
import sys
from functools import partial
import logging
import csv
import threading
import play_scraper
import json

AppsInfo = 'apps_info.csv'
GOOGLE_PLAY_APPS_TXT = 'free_apps.txt'
download_folder = "\\download"
num_process = 1

gpc = gplaycli.GPlaycli()


def print_app_info(apps):
    """
    Print the application information that was retrieve from Google Play
    Args:
        A list of application information that was retrieved using GPLAYCLI
    Returns:
        NIL
    Raises:
        NIL

    """
    print("App Title : " + apps[0])
    print("Creator : " + apps[1])
    print("Size : " + apps[2])
    print("Downloads : " + apps[3])
    print("Last Update : " + apps[4])
    print("App ID : " + apps[5])
    print("Version Code : " + str(apps[6]))
    print("Rating : " + str(apps[7]))


def read_apps_name():
    """
    Get the names of application from GOOGLE_PLAY_APPS_TXT
    Args:
    Returns:
        A list of application name that was retrieved from GOOGLE_PLAY_APPS_TXT
        
    Raises:
        NIL

    """
    apps_name_list = []
    with open(GOOGLE_PLAY_APPS_TXT) as apps_name:
        for line in apps_name:
            line = line[:-1]  # windows: -1,linux:-2
            apps_name_list.append(line)

    return apps_name_list


def perform(*apps_list):
    for app in apps_list:
        compare_apps_version(app)


def compare_apps_version(apps_name):
    """
    Compare the application name by searching the database and googleplay.
    If their version is different, then the download will be started and the
    apk will be downloaded into the download_folder
    Args:
    Returns:
        NIL
        
    Raises:
        NIL

    """
    try:
        print("\nSearching for " + apps_name)
        search_result = gpc.search(apps_name)
        if search_result is None:
            search_result = []
            print("not in google")
            return
        print("There are " + str(len(search_result) - 1) + " results")
        result_valid = check_app_name(search_result, apps_name)

        if (result_valid) != -1:
            print("\n")
            with open(AppsInfo, 'r', encoding='utf-8') as csv_file:
                apps_list = csv.DictReader(csv_file, delimiter=',', quotechar='"')
                printing_cursor = [row for row in apps_list if row["App ID"] == apps_name]
                flag = 0  # if flag==0,download new apk
                for apps in printing_cursor:
                    if int(apps['Version Code']) == search_result[result_valid][6]:
                        print("Same version detected.No need to download " + apps_name)
                        flag = 1
                if flag == 0:
                    with open(AppsInfo, 'a+', encoding='utf-8', newline='') as fp:
                        writer = csv.writer(fp)
                        details = play_scraper.details(apps_name)
                        description = details.get('description')
                        app_info_row = search_result[result_valid]
                        app_info_row.append(description)
                        writer.writerow(app_info_row)
                    fp.close()
                    temp_list = []
                    temp_list.append(search_result[result_valid][5])
                    downloaded_file = os.path.join(download_folder, temp_list[0] + ".apk")
                    renamed_file = os.path.join(download_folder,
                                                temp_list[0] + "_" + str(search_result[result_valid][6]) + ".apk")

                    if not os.path.exists(renamed_file):
                        download_apps(gpc, downloaded_file, temp_list)

                        if os.path.exists(downloaded_file):
                            print("renamed")
                            os.rename(downloaded_file, renamed_file)
                        # raw_input("WAIT")
                    else:
                        print("file existed")
            csv_file.close()
        else:
            print("There are no " + apps_name + " in google stores...")
            # time.sleep(5)
    except Exception as ex:
        print("exception: " + str(ex))


def download_apps(gpc, downloaded_file, app_name_list):
    """
    Download the app_name from googleplay
    Please note that the app_name_list is actually a list 
    Args:
        A list of application list and the gplaycli instance
    Returns:        
    Raises:

    """
    print("Download for " + str(app_name_list[0]) + " is starting...")
    # newpara=(app_name_list[0],downloaded_file)
    # tod_list=[]
    # tod_list.append(newpara)
    gpc.download(app_name_list)
    print("Download for " + str(app_name_list[0]) + " is completed...")


def check_app_name(search_result, apps_name):
    """
    Compare the apps_name with the search_result which was retrieved from
    the googleplay(gplaycli)
    This method exists as not all apps_name existed within the search_result.
    For example, com.abc.def might not be in the search_result but other similar
    packages name might be inside the search_result
    Args:
        search_result = a return value from gplaycli.search()
        apps_name = an apps name
    Returns:
        Return the index of the apps_name if it existed, else it will return
        -1
    Raises:

    """
    for x in range(0, len(search_result)):
        if search_result[x][5] == apps_name:
            print_app_info(search_result[x])
            return x

    print("No same apps name found")
    return -1


def main():
    # help(gplaycli)
    # dir(gplaycli)

    if len(sys.argv) > 2:
        global download_folder
        download_folder = sys.argv[1]
        global num_process
        num_process = int(sys.argv[2])
    gpc.download_folder = download_folder
    # Debug Messages
    print("Download folder : " + download_folder)
    print("Getting apps information from free_apps.txt")

    # Read from the files
    apps_name_list = read_apps_name()
    print("Apps name is stored in apps_name_list")

    # Connect to Google Play
    print("Connecting to Google Play through gplaycli")
    success, error = gpc.connect()
    if not success:
        print(error)
        return
    # gpc.download_folder(download_folder) # there is no func now
    print("Google Play Connected")

    # print(gpc.search("360"))
    # gpc.download(['org.mozilla.focus','org.mozilla.firefox'])

    for apps_tod in apps_name_list:
        compare_apps_version(apps_tod)
    # Creating Pool of Processes
    # print("Creating a pool of " + str(num_process) + " process")
    # pool = Pool(int(num_process))
    # pool.map(compare_apps_version, apps_name_list)
    # pool.close()
    # pool.join()
    #
    # per_thread = len(apps_name_list) // num_process #need '//' to get interger
    # threads = []
    # for i in range(num_process):
    #     if i == num_process - 1:
    #         t = threading.Thread(target=perform, args=(apps_name_list[i * per_thread:]))
    #     else:
    #         t = threading.Thread(target=perform, args=(apps_name_list[i * per_thread:i * per_thread + per_thread]))
    #     threads.append(t)
    #
    # for i in range(num_process):
    #     threads[i].start()
    #
    # for i in range(num_process):
    #     threads[i].join()
    #

    print('The update process is completed')


# Main Method of the Script
if __name__ == "__main__":
    main()
