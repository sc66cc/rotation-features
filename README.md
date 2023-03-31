## 《计算古经纬度简易脚本》

  相信不少做地质研究的同学都有计算古经纬度做古地理图数据投点的需求，一般都是通过读取数据点的经纬度生成Shapefile在GPlates、ArcGIS处理来实现，这种方式显然太繁琐且低效了。我参考了国外作者 Alexandre Pohl 的博客，写了一个简易的Python脚本来实现这一功能，只需要输入带有经纬度、重建年龄的表格，计算的古经纬度结果可以直接附加到新的表格中，下面是使用的教程。
  
  
## Step 1 准备数据

输入的文件格式要求为逗号分隔的csv格式，编码方式选择`utf-8`，在输入的csv文件中，对表头的命名有以下规则

    经度：lng，纬度：lat，重建年龄：reconstruction_age
如下图所示

<img src="https://user-images.githubusercontent.com/90812672/227698606-0e30d528-14b6-42fa-b63a-7ecda749a01b.jpg" width="200" height="230">


## Step 2 配置conda环境

conda是一个常用的开源库管理、环境管理软件，我们选择在 conda 中创建虚拟环境来运行脚本，脚本的依赖库为pygplates, pandas, numpy，下面是使用conda创建相应的虚拟环境步骤。

### 1. 安装miniconda

miniconda是一个精简安装版conda，只包括conda, python及相关的依赖。miniconda下载地址：[Miniconda - Download](https://docs.conda.io/en/latest/miniconda.html)

打开终端控制台（Windows系统，在脚本所在的文件夹地址栏中输入cmd），输入conda 查看是否安装成功，如成功为以下状态。

<img src="https://user-images.githubusercontent.com/90812672/229004019-7011845e-e5c1-4897-9607-d8f7027afeaa.jpg" width="500" height="300">



### 2. 安装相关依赖

打开终端控制台，输入下列命令

**创建虚拟环境**

```
conda create -n pygplates_py38 python=3.8
```

**激活虚拟环境**

Windows:

```
activate pygplates_py38
```

Linux or macOS:

```
conda activate pygplates_py38
```                                                                                                                         

**安装相关依赖包**

```
conda install -c conda-forge pygplates pandas numpy
```

**检查环境**

```
python -c "import pygplates;import pandas;import numpy; print(pygplates.__version__)"
```

如果未出现任何报错信息，并输出了`pygplates`版本，则说明该脚本的运行环境配置成功。

    
## Step 3 运行脚本

配置完运行环境后，使用文本编辑工具打开`RotFeatures.py`，替换 `simple.csv` 文件名为你自己数据的文件名

<img src="https://user-images.githubusercontent.com/90812672/227700210-40816ae1-5a0f-463e-9059-71fc077d6d23.jpg" width="550" height="150">


把数据、脚本放在同一个文件夹下，然后在文件夹的地址栏输入`cmd`调出控制台，激活先前配置好的conda虚拟环境，输入以下命令：

    python RotFeatures.py
    
点击回车
如果控制台输出以下内容，代表脚本执行成功。

    xx/xxx (x.x%) cannot complete the rotation.
    Saving to file: xxxx_rotatedScotese2016.csv
    
新的文件将以  原文件名_rotatedScotese2016.csv  保存在同一目录下


## 说明

默认使用 Scotese, 2016 板块重建模型，该脚本还支持自定义指定板块重建模型和板块静态多边形文件，通过指定rotate_points()函数的参数 `model="xxxx"`来实现。

原文件中包含了相关的模型文件，完整的板块重建模型下载地址：https://www.earthbyte.org/paleodem-resource-scotese-and-wright-2018/

该脚本相关文件列表

    PALEOMAP_PlateModel.rot # Scotese, 2016 板块重建模型旋转文件
    PALEOMAP_PlatePolygons.gpml # Scotese, 2016 板块重建模型静态多边形文件
    Seton_etal_ESR2012_2012.1.rot # Seton et al., 2012 用于计算洋壳上点的模型文件
    Seton_etal_ESR2012_StaticPolygons_2012.1.gpmlz # Seton et al., 2012 用于计算洋壳上点的静态多边形文件
    RotFeatures.py # python脚本
    simple.csv # 样例数据
    simple_rotatedScotese2016.csv # 样例数据运行结果
    

本脚本作者：程汉 中国地质大学（北京）

参考代码原作者 Alexandre Pohl  (CNRS Researcher)

原代码参考地址：https://paleoclim-cnrs.github.io/documentation-processing/pyGplates/#python-code
