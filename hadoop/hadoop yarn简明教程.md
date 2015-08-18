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

4. yarn基本架构
   YARN 主要由 ResourceManager、NodeManager、ApplicationMaster和 Container 等几个组件构成。
   1. ResourceManager ( RM )
      它主要由两个组件构成:调度器(Scheduler)和应用程序管理器(Applications Manager,ASM)。
      1. 调度器   调度器根据容量、队列等限制条件(如每个队列分配一定的资源,最多执行一定数量的作业等),将系统中的资源分配给各个正在运行的应用程序。
      2. 应用程序管理器  应用程序管理器负责管理整个系统中所有应用程序,包括应用程序提交、与调度器协商
资源以启动 ApplicationMaster、监控 ApplicationMaster 运行状态并在失败时重新启动它等。
   2. ApplicationMaster ( AM )
      用户提交的每个应用程序均包含一个 AM,主要功能包括:
      与 RM 调度器协商以获取资源(用 Container 表示);
      将得到的任务进一步分配给内部的任务;
      与 NM 通信以启动 / 停止任务;
      监控所有任务运行状态,并在任务运行失败时重新为任务申请资源以重启任务。
   3. NodeManager ( NM ) 
       NM 是每个节点上的资源和任务管理器,一方面,它会定时地向 RM 汇报本节点上的资源使用情况和各个 Container 的运行状态;另一方面,它接收并处理来自 AM 的 Container启动 /停止等各种请求。
   4. Container  
      Container是 YARN 中 的 资 源 抽 象, 它 封 装 了 某 个 节 点 上 的 多 维 度 资 源, 如 内存、CPU、磁盘、网络等,当 AM 向 RM 申请资源时,RM 为 AM 返回的资源便是用 Container表示的。   

5. yarn的工作流程
   1. 用 户 向 YARN 中 提 交 应 用 程 序, 其 中 包 括 ApplicationMaster 程 序、 启 动ApplicationMaster 的命令、用户程序等。
   2. ResourceManager 为 该 应 用 程 序 分 配 第 一 个 Container, 并 与 对 应 的 Node-Manager 通信,要求它在这个 Container 中启动应用程序的 ApplicationMaster。
   3. ApplicationMaster 首 先 向 ResourceManager 注 册, 这 样 用 户 可 以 直 接 通 过ResourceManager查看应用程序的运行状态,然后它将为各个任务申请资源,并监控它的运行状态,直到运行结束,即重复步骤 4~7。
   4. ApplicationMaster采用轮询的方式通过 RPC 协议向 ResourceManager 申请和领取资源。
   5. 一旦 ApplicationMaster 申请到资源后,便与对应的 NodeManager 通信,要求它启动任务。
   6. NodeManager 为任务设置好运行环境(包括环境变量、JAR包、二进制程序等)后,将任务启动命令写到一个脚本中,并通过运行该脚本启动任务。
   7. 各个任务通过某个 RPC 协议向 ApplicationMaster 汇报自己的状态和进度,以让 ApplicationMaster 随时掌握各个任务的运行状态,从而可以在任务失败时重新启动任务。在应用程序运行过程中,用户可随时通过 RPC 向 ApplicationMaster 查询应用程序的当前运行状态。
   8. 应用程序运行完成后, ApplicationMaster 向 ResourceManager 注销并关闭自己。
   
