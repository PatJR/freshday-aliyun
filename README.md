# 天天生鲜项目

## **该项目是基于 B/S结构的B2C电商项目**

> B/S--(Browser/Server)
> B/S架构即浏览器和服务器架构模式。对C/S架构的一种变化或者改进的架构。在这种架构下，用户工作界面是通过浏览器来实现，极少部分事务逻辑在前端(Browser)实现，但是主要事务逻辑在服务器端(Server)实现，形成所谓三层3-tier（界面层/业务逻辑层/数据访问层）结构。B/S架构是WEB兴起后的一种网络架构模式，WEB浏览器是客户端最主要的应用软件。这种模式统一了客户端，将系统功能实现的核心部分集中到服务器上，简化了系统的开发、维护和使用。客户机上只要安装一个浏览器（Browser），如Netscape Navigator或Internet Explorer，服务器安装Oracle、Sybase、Informix或 SQL Server等数据库。浏览器通过Web Server同数据库进行数据交互。 这样就大大简化了客户端电脑载荷，减轻了系统维护与升级的成本和工作量，降低了用户的总体成本(TCO)。


**注：** 教程版本使用的是python3.3、 Django1.8，该版本为Django2.2部分代码与1.8有出入，功能实现一样。详情查看Django2.2文档

## 技术栈

- **python 3.6**

- **Django 2.2**
- **[Haystack](http://haystacksearch.org/)(全文检索框架)**
- [Whoosh(纯Python编写的全文搜索引擎)](https://whoosh.readthedocs.io/en/latest/)

- **MySQL**
- **Redis**
- **[FastDFS](https://github.com/happyfish100/fastdfs)**(分布式文件系统)
- **Nginx**
- **uwsgi**

## 技术架构

### 技术框架

<image src="https://github.com/PatJR/MEDIA/blob/master/dailyfresh/framework.png" width="80%">
  
 ### 网络拓扑
 <image src="https://github.com/PatJR/MEDIA/blob/master/dailyfresh/%E7%BD%91%E7%BB%9C%E6%8B%93%E6%89%91.jpg">


## 业务模块
<image src="https://github.com/PatJR/MEDIA/blob/master/dailyfresh/%E4%B8%9A%E5%8A%A1%E6%A8%A1%E5%9D%97.png">
