

根据crawler中的gp_periodical_downloads.py文件改的，主要是因为gplaycli版本更新用不了

# 环境依赖：

* gplaycli

  `pip install gplaycli`
* play_scraper

  `pip install play_scraper`

* anaconda

# 各个文件说明：

* free_apps.txt

  写下要下载的app包名，回车键下一个

* apps_info.csv

  已经下载过的app文件的信息。

  在下载新的apk文件时会先查找该csv文件是否有相应的版本，没有就下载

* init_csv.py

  删除原有的apps_info.csv文件的内容并初始化列名，使用前运行一次就行

* gp_downloads.py

  **程序运行文件，直接run就可以**

  默认下载在程序所在盘的download文件夹里，如果需要更改，把该文件开头的:`download_folder = "\\download"`改了就可以了

* gplaycli.conf和token

  使用gplaycli需要的配置文件，不需要改