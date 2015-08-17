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
  3. 计算作业的输入划分，并将划分信息写入job.split文件。
  4. 将运行作业所需要的资源——包括jar包、配置文件盒计算所得的输入划分等复制到hdfs上。
  
2. 初始化作业
   jobtracker会把作业放入内部的taskscheduler变量中，进行调度，一般FIFO调度方式。
  1. 从hdfs中读取作业对应的job.split，得到输入数据的划分信息。
  2. 创建初始化map任务和reduce任务，根据split个数设定map，根据jobconf中的mapred.reduce.tasks配置设定reduce个数。
  3. 创建2个初始化task。
  
3. 分配任务
  tasktracker向jobtracker发送心跳，并请求分配任务。
  
4. 执行任务
  1. 将任务运行所必需的数据、配置信息、程序代码从hdfs复制到tasktracker本地。
  2. 调用launchtaskforjob启动任务。
  
5. 更新任务执行进度和状态
   通过计数器标志告知tasktracker当前的任务状态。

6. 完成作业
   当jobtracker接收到最后一个任务的已完成通知后，便把作业的状态设置为“成功”。

##错误处理机制

1.硬件故障
  1. jobtracker故障 采用领导选举算法重新确定jobtracker
  2. tasktracker故障 
     1. 如果tasktracker在1分钟没有和jobtracker通信，则要求该tasktracker上的任务立即返回，并要求其他tasktracker重新执行未完成的map任务或者reduce任务。（map任务必须重新执行，reduce可以只执行未完成的）
2. 任务失败
   如果任务执行失败，jvm进程会自动退出，并向父进程发送错误，写入log，如果主进程没有收到进程进度更新，也会将任务标记失败，杀死程序对应的进程。通过心跳机制告诉jobtracker任务失败，jobtracker重新分配任务，重复4次失败则整个作业失败。

##作业调度机制
1. 先进先出 作业提交的顺序来运行
2. 公平调度 每个用户一个独立的作业池，使用公平共享的方法在运行作业间共享容量，还可以为作业设置最小资源和最大并行作业数，避免塞满磁盘空间。

##shuffle和排序
shuffle过程包含在map和reduce两端中。
1. map端
   当map任务的环形内存缓冲区达到阀值时，需要创建spill文件，然后按照key值排序，再执行combine类合并后写入。map任务执行完毕后合并spill文件（每个key都会取模来决定最终归属的reduce，这里称为分区。文件按照分区排序合并）
2. reduce端
  每完成一个map任务，jobtracker告知map输出位置，reduce复制输出到本地同时进行合并，保持数据原来的顺序。最后进行reduce处理。

##任务执行
1. 推测式执行
   如果某个任务所在的tasktracker节点配置低或者cpu负载过高，导致任务执行速度慢，则jobtracker会重启一个新的备份任务，哪个先执行完就把另外一个kill掉。
2. 任务jvm重用
   通过设置jvm运行任务数来重用jvm，解决新建多个jvm的消耗。
3. 跳过坏记录


##hadoop的I/O操作
1. I/O操作中的数据检查
   hadoopshiyongcrc-32进行数据完整性检查。
   1. 对本地文件I/O的检查 每当hadoop创建文件a时，都会在同一目录下创建.a.crc，记录了文件a的校验和。默认每512字节生成一个校验和。
   2. 对hdfs的I/O数据进行检查 
     1. datanode接收数据后存储数据前 hadoop会生成一条数据管线，数据在传送给主datanode的同时也会向备份datanode传送，3个备份形成时间差不多。
     2. 客户端读取datanode上的数据时进行校验和检验
     3. datanode后台守护进程定期检查 
   3. 数据恢复策略 如果发现数据块失效，则datanode和namenode都会尝试修复，修复成功后设置标签，避免重新修复。

2. 数据的压缩 gzip、bzip2、zlib（bzip2支持文件分割）
3. 数据的I/O序列化操作
   序列化有两个目的：
   1. 进程间通信
   2. 数据持久性存储
   hadoop采用rpc来实现进程间通信。
4. 针对mapreduce的文件类
   1. sequencefile类 记录的是key/value对列表，是序列化后的二进制文件，不能直接查看。
   2. mapfile类 与sequencefile类似，但生成的结果多一个索引文件


##下一代mapreduce：yarn

1. mapreduce的局限性
  1. jobtracker单点瓶颈 随着业务增长，jobtracker的内存和带宽会不够。
  2. tasktracker作业配置太简单
  3. 作业延迟过高 jobtracker需要根据tasktracker汇报的执行情况来分配作业
  4. 编程框架不够灵活
   
2. yarn的主要思想
  1. 将jobtracker的资源管理和作业管理分离

  
##hdfs详解
1. 主要特点
  1. 处理超大文件 MB，TB
  2. 流式访问数据 读取大文件不需要特别大的内存
  3. 运行于廉价商用机器集群上  意味着节点故障率比较高
2. 局限
  1. 不适合低延迟的数据访问
  2. 无法高效存储大量小文件 文件的索引等元数据由namenode存储，namenode内存大小有限。
  3. 不支持多用户写入及任意修改文件
1. 相关概念
   1. 块
      类似于磁盘块，hdfs也有块的概念，大小默认为64MB。hdfs中的文件分块存储。
2. api操作示例
```

    //创建新文件
    public static void createFile(String dst , byte[] contents) throws IOException{
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        Path dstPath = new Path(dst); //目标路径
        //打开一个输出流
        FSDataOutputStream outputStream = fs.create(dstPath);
        outputStream.write(contents);
        outputStream.close();
        fs.close();
        System.out.println("文件创建成功！");

    
    //上传本地文件
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        Path srcPath = new Path(src); //原路径
        Path dstPath = new Path(dst); //目标路径
        //调用文件系统的文件复制函数,前面参数是指是否删除原文件，true为删除，默认为false
        fs.copyFromLocalFile(false,srcPath, dstPath);
        
        //打印文件路径
        System.out.println("Upload to "+conf.get("fs.default.name"));
        System.out.println("------------list files------------"+"\n");
        FileStatus [] fileStatus = fs.listStatus(dstPath);
        for (FileStatus file : fileStatus) 
        {
            System.out.println(file.getPath());
        }
        fs.close();

    //文件重命名
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        Path oldPath = new Path(oldName);
        Path newPath = new Path(newName);
        boolean isok = fs.rename(oldPath, newPath);
        if(isok){
            System.out.println("rename ok!");
        }else{
            System.out.println("rename failure");
        }
        fs.close();

    //删除文件
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        Path path = new Path(filePath);
        boolean isok = fs.deleteOnExit(path);
        if(isok){
            System.out.println("delete ok!");
        }else{
            System.out.println("delete failure");
        }
        fs.close();
    
    //创建目录

        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        Path srcPath = new Path(path);
        boolean isok = fs.mkdirs(srcPath);
        if(isok){
            System.out.println("create dir ok!");
        }else{
            System.out.println("create dir failure");
        }
        fs.close();

    
   //读取文件的内容

        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        Path srcPath = new Path(filePath);
        InputStream in = null;
        try {
            in = fs.open(srcPath);
            IOUtils.copyBytes(in, System.out, 4096, false); //复制到标准输出流
        } finally {
            IOUtils.closeStream(in);
        }

```

##mapreduce测试
依赖：junit4, mockito1.10,mrunit1.1,powermock1.62

```
import java.util.ArrayList;
import java.util.List;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mrunit.mapreduce.MapDriver;
import org.apache.hadoop.mrunit.mapreduce.MapReduceDriver;
import org.apache.hadoop.mrunit.mapreduce.ReduceDriver;
import org.junit.Before;
import org.junit.Test;
 
public class SMSCDRMapperReducerTest {
  MapDriver<LongWritable, Text, Text, IntWritable> mapDriver;
  ReduceDriver<Text, IntWritable, Text, IntWritable> reduceDriver;
  MapReduceDriver<LongWritable, Text, Text, IntWritable, Text, IntWritable> mapReduceDriver;
 
  @Before
  public void setUp() {
    SMSCDRMapper mapper = new SMSCDRMapper();
    SMSCDRReducer reducer = new SMSCDRReducer();
    mapDriver = MapDriver.newMapDriver(mapper);
    reduceDriver = ReduceDriver.newReduceDriver(reducer);
    mapReduceDriver = MapReduceDriver.newMapReduceDriver(mapper, reducer);
  }
 
  @Test
  public void testMapper() {
    mapDriver.withInput(new LongWritable(), new Text(
        "655209;1;796764372490213;804422938115889;6"));
    mapDriver.withOutput(new Text("6"), new IntWritable(1));
    mapDriver.runTest();
  }
 
  @Test
  public void testReducer() {
    List<IntWritable> values = new ArrayList<IntWritable>();
    values.add(new IntWritable(1));
    values.add(new IntWritable(1));
    reduceDriver.withInput(new Text("6"), values);
    reduceDriver.withOutput(new Text("6"), new IntWritable(2));
    reduceDriver.runTest();
  }
   
  @Test
  public void testMapReduce() {
    mapReduceDriver.withInput(new LongWritable(), new Text(
              "655209;1;796764372490213;804422938115889;6"));
    List<IntWritable> values = new ArrayList<IntWritable>();
    values.add(new IntWritable(1));
    values.add(new IntWritable(1));
    mapReduceDriver.withOutput(new Text("6"), new IntWritable(2));
    mapReduceDriver.runTest();
  }
}
```
