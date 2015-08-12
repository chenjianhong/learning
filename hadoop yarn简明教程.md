#yarn架构设计与实现原理
##产生的背景
1. mrv1的局限性
   1. 扩展性差 jobtracker限制
   2. 可靠性差 jobtracker单点故障
   3. 资源利用率低 槽位之间的资源无法共享
   4. 无法支持多种计算框架
   
2. 轻量级弹性计算平台
   数据密集型应用计算框架：
   1. mapreduce
   2. storm
   3. spark
   4. s4
   在大部分公司中，几种框架可能同时被采用。所以需要一个公共集群，共享资源，具备资源隔离功能，yarn便是这样的轻量级弹性计算平台。
   好处：
   1. 资源利用率高
   2. 运维成本低
   3. 数据共享
   
3. 术语
   1. hadoop 1.0
      由hdfs和mapreduce组成，对应hadoop版本0.20,1.x,0.21.x,0.22.x,cdh3
   2. hadoop 2.0
      jobtracker分离成ResourceManager,ApplicationMaster。前者负责所有应用程序的资源分配，后者仅负责管理一个应用程序。yarn诞生。对应版本0.23.x,2.x,cdh4。
   3. MRV2
      具有与MRV1相同的编程模型和数据处理引擎，唯一不同的是运行环境。MRV2运行在yarn上。
   4. HDFS Federation
      hadoop2.0对hdfs进行了改进，namenode可以横向扩展多个，每个管理一部分目录，进而产生了Federation。增强了hdfs的扩展性，新增了隔离性。
