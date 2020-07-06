

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

* search_keyword.py

  根据keyword得到搜索结果，并将结果中的app的package name写入free_apps.txt。

  修改开头的`KEYWORD`选择不同的keyword搜索，修改`NUM`选择前num个结果

  可以追加写入

* gp_downloads.py

  **程序运行文件，直接run就可以**

  默认下载在程序所在盘的download文件夹里，如果需要更改，把该文件开头的:`download_folder = "\\download"`改了就可以了

  第一个下载apk会报runtimewarning，不影响运行

* gplaycli.conf和token

  使用gplaycli需要的配置文件，不需要改

# 运行顺序

①init_csv.py 第一次运行，以后使用就从②开始

②search_keyword.py 可以更换keyword多次运行

③手动加入free_apps.txt

④gp_downloads.py



* 没有下载成功的app会在!!exception!!那几行中print出来，（可能原因是和google play连接太多的原因），到时候重新运行gp_downloads即可





 

