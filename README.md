## 《计算古经纬度简易脚本》

  相信不少做地质研究的同学都有计算古经纬度做古地理图数据投点的需求，一般都是通过读取数据点的经纬度生成Shapefile在GPlates、ArcGIS处理来实现，这种方式显然太繁琐且低效了。我参考了国外作者 Alexandre Pohl 的博客，写了一个简易的Python脚本来实现这一功能，只需要输入带有经纬度、重建年龄的表格，计算的古经纬度结果可以直接附加到新的表格中，下面是使用的教程。
  
  
## Step 1 准备数据

在输入的csv文件中，对表头的命名有以下规则

    经度：lng，纬度：lat，重建年龄：reconstruction_age
如下图所示

<img src="https://user-images.githubusercontent.com/90812672/227698606-0e30d528-14b6-42fa-b63a-7ecda749a01b.jpg" width="200" height="230">


## Step 2 准备环境

该脚本使用python语言编写，脚本运行环境为pygplates, pandas, numpy 这三个库，下面是安装库的相关方式。

1. pygplates：由于pygplates库不能直接通过pip install pygplates直接安装，需要到EarthByte官网上按照他们提供的方式去安装。

官网地址    https://www.gplates.org/docs/pygplates/pygplates_getting_started.html#installation

2. 其他库的安装：
`pip install pandas numpy`

检查环境：在你的终端控制台输入 `python` 激活python程序，输入以下命令

    import pygplates
    import pandas
    import numpy
    
如果没有出现任何报错信息，表示环境配置成功。
    
## Step 3 运行脚本

配置完运行环境后，使用文本编辑工具打开`RotFeatures.py`，替换 `simple.csv` 文件名为你自己数据的文件名

<img src="https://user-images.githubusercontent.com/90812672/227700210-40816ae1-5a0f-463e-9059-71fc077d6d23.jpg" width="550" height="150">


把数据、脚本放在同一个文件夹下，然后在文件夹的地址栏输入`cmd`调出控制台，输入以下命令：

    python RotFeatures.py
    
点击回车
如果控制台输出以下内容，代表脚本执行成功。

    xx/xxx (x.x%) cannot complete the rotation.
    Saving to file: xxxx_rotatedScotese2016.csv
    
新的文件将以  原文件名_rotatedScotese2016.csv


## 说明

默认使用 Scotese, 2016 板块重建模型，该脚本还支持自定义板块重建模型和板块静态多边形文件，通过指定rot函数的参数 `rotation_file='xxx.rot',static_polygons='xxx.gpml'`来实现。

原文件中包含了相关的模型文件，完整的板块重建模型下载地址：https://www.earthbyte.org/paleodem-resource-scotese-and-wright-2018/

原文件列表

    PALEOMAP_PlateModel.rot
    PALEOMAP_PlatePolygons.gpml
    RotFeatures.py

本脚本作者：程汉 中国地质大学（北京）

参考代码原作者 Alexandre Pohl

原代码参考地址：https://paleoclim-cnrs.github.io/documentation-processing/pyGplates/#python-code
