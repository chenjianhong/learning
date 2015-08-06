#hadoop简要教程

##概述
1. hadoop是apache软件基金会旗下的一个开源分布式计算平台。
2. 大数据的特点4v，volume（量大）、variety（种类多）、value（价值密度低）、velocity（处理速度快）
3. 云计算因大数据而存在，hadoop连接了大数据和云计算。
4. 国内外hadoop的应用现状
  1. yahoo 总节点超过42000，单master节点有4500个节点。总集群量350pb
  2. facebook 1440个节点，15pb容量
  3. 百度 集群10个，单集群超过2800台机器节点，100pb存储
  4. 阿里 3200台节点，60pb存储

##优点
1. 高可靠性
2. 高扩展性
3. 高效性
4. 高容错性

##hadoop体系结构

hdfs和mapreduce是hadoop的两大核心。
1. hdfs体系结构。
   1. hdfs采用了主从结构模型，一个hdfs集群由一个namenode和若干个datanode组成。
   2. namenode作为主服务器，管理文件系统的命名空间和客户端对文件的访问操作。
   3. datanode管理存储的数据。
2. mapreduce体系结构
   1. 由一个单独运行在主节点的jobtracker和运行在每个集群从节点的tasktracker组成。
   2. 主节点负责调度一个作业的所有任务，监控执行情况，重新执行失败的任务。
   3. 从节点仅负责由主节点指派的任务。
  
 
##hadoop集群安全策略
1. 用户权限管理 
2. hdfs安全策略
3. mapreduce安全策略

##hadoop的安装与配置
1. 安装jdk
2. 配置JAVA_HOME,CLASSPATH,PATH环境变量。
3. 安装ssh，创建公钥文件，配置ssh。
4. 下载hadoop
5. 配置hadoop
6. 格式化hadoop文件系统hdfs
7. 验证安装是否成功

##配置hadoop cluster
1. 配置/etc/hosts及/etc/hostname
2. 配置ssh可免密码登录
3. 配置所有节点的hadoop-env.sh文件指定JAVA_HOME
4. 配置所有节点的core-site.xml文件
   1. 指定namenode的ip地址和端口，fs.default.name。
   2. 指定hadoop.tmp.dir，节点的block数据和元数据都默认存放在这个目录。
5. 配置hdfs-site.xml文件，指定文件备份数，元数据和datanode数据目录。
6. 配置map-site.xml文件，指定jobtracker地址。
7. 配置masters，指定master
8. 配置slaves，指定slaves
9. 启动hadoop

##mapreduce计算模型

1.每个mr任务都被初始化为一个job，每个job分为：map阶段，reduce阶段
2.map函数接受<key,value>形式输入，产生<key,value>形式输出
3.hadoop负责将所有具有相同key值的value集合到一起传递给reduce函数
4.reduce函数接受<key,(list of values)>形式的输入，产生<key,value>形式输出

###inputFormat，inputSplit，outputformat
通过指定inputformat生成inputsplit。数据传送给map后，map通过inputformat生成recordreader，再获取<key,value>对
hadoop默认使用TextInputFormat输入方法，其中每个文件或者其中一部分会单独作为map的输入，每行都会生成一条记录。key是记录偏移量，value是每行内容。
outputformat定义输出格式。

###mapreduce任务优化
1. 任务粒度
2. 数据预处理和inputsplit的大小 hadoop擅长处理少量大数据，不是大量小数据，可以先合并。
3. map和reduce任务的数量 reduce任务应该是reduce任务槽的0.95-1.75倍
4. conbine函数 用于本地合并，减少网络I/O消耗
5. 压缩 一般对map的中间输出进行压缩
6. 自定义数据类型 减少数据计算时间

##hadoop流
hadoop流提供了一个API，允许使用任何语言写map和reduce函数。
1.原理
  每个map和reduce任务会以独立进程启动，并且输入和输出都依靠标准输入和输出。 默认情况下，一行中第一个tab之前的部分作为key，之后的（不包括tab）作为value。如果没有tab，整行作为key值，value值为null。reduce的输入是map输出后根据key排序好的。

##jobtracker页面
   页面主要包括五个部分。
   1. hadoop安装的详细信息。版本号、编译完成时间、jobtracker当前运行状态和开始时间。
   2. 集群的总结信息。集群容量及使用情况，运行的mr数量，当前的可用tasktracker数量等。
   3. 正在运行的工作日程表
   4. 正在运行、完成、失败的工作
   5. jobtracker的历史信息。

##复杂的map和reduce函数
1. setup函数 每个任务启动后只调用一次
2. cleanup函数 每个任务启动后只调用一次
3. 使用DistributedCache只读缓存文件
4. 链接mapreduce job

##mapreduce作业的执行流程
代码编写-作业配置-作业提交-map任务分配和执行-处理中间结果-reduce任务分配和执行-作业完成。
涉及4个独立的实体：
1. 客户端 编写mr代码，配置作业，提交作业
2. jobtracker 初始化作业，分配作业，协调作业的执行
3. tasktracker 执行map或reduce任务，保持和jobtracker通信
4. hdfs 保持作业数据，配置信息。

1. 提交作业
  1. 通过jobtracker获取作业id
  2. 检查相关路径是否存在
