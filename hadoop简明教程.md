#hadoop简要教程

##概述
1. hadoop是apache软件基金会旗下的一个开源分布式计算平台。

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
