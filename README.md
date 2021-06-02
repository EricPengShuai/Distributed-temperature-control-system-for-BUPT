# 分布式温控系统

* [Distributed-temperature-control-system-for-BUPT 工程说明文件](#分布式温控系统)  
&emsp;* [开发语言](#开发语言)  
&emsp;* [框架选择](#框架选择)  
&emsp;* [运行方式](#运行方式)  
&emsp;&emsp;* [前端运行说明](#前端运行说明)  
&emsp;&emsp;* [后端运行说明](#后端运行说明)  
&emsp;&emsp;&emsp;* [数据库版本](#数据库版本)  
&emsp;&emsp;&emsp;* [数据库建库脚本文件](#数据库建库脚本文件)  
&emsp;* [环境说明](#环境说明)  
&emsp;&emsp;* [后端依赖](#后端依赖)  
&emsp;&emsp;* [前端依赖](#前端依赖)  

## 开发语言
基于`python3.8`以及`JavaScript`开发



## 框架选择

前端`JavaScript-Vue`，后端`python-flask`



## 运行方式

具体可以参考`AIR_CONDITIONER`文件夹中的`run.sh`脚本

### 前端运行说明

在`front_end`目录下运行命令：

1. `npm install`：安装相关依赖包

   - 可能出现某些依赖等级需要提升的问题，按照**npm**提示安装升级即可

2. `npm run serve`：启动前端服务

   

![front_end-npm-run-serve](https://github.com/pengshuai98/Distributed-temperature-control-system-for-BUPT/blob/master/README.assets/npm-run-%20serve.png)

随后点击其中一个URL即可访问本分布式空调管理系统的界面

### 后端运行说明

#### 数据库版本
>`mysql 8.0.19 Homebrew`

![mysql-version](https://github.com/pengshuai98/Distributed-temperature-control-system-for-BUPT/blob/master/README.assets/mysql-version.png)

#### 数据库建库脚本文件
>`mysqlTable.py`已集成到代码中。

![mysql-table-code](https://github.com/pengshuai98/Distributed-temperature-control-system-for-BUPT/blob/master/README.assets/code.png)



## 环境说明

### 后端依赖

需要使用`pip3`安装以下包。

```
PyMySQL==0.9.3
Flask_Cors==3.0.8
Flask==1.1.2
Flask_SocketIO==4.3.0
```

### 前端依赖

参考`./AIR_CONDITIONER/front_end/package.json`文件
