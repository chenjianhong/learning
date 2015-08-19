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
2. 优缺点
    优点
        可以使用自己喜欢的语言来编写MapReduce程序（python）
        不需要像写Java的MR程序那样import一大堆库，在代码里做一大堆配置，代码量显著减少
        因为没有库的依赖，调试方便，并且可以脱离Hadoop先在本地用管道模拟调试
    缺点
        只能通过命令行参数来控制MapReduce框架，不像Java的程序那样可以在代码里使用API，控制力比较弱
        因为中间隔着一层处理，效率会比较慢
示例：
1.执行python脚本
```
#coding: utf-8
"""
Some description here...
"""

import sys

def main():
    item_count = dict()
    for line in sys.stdin:
        items = line.strip().split(' ')
        item_count[items[0]] = item_count.get(items[0],0) + 1
    for sub in item_count:
        print '%s\t%s\n'%(sub,item_count[sub])


if __name__ == "__main__":
    main()
```
```
hadoop  jar <hadoop_home>/share/hadoop/tools/lib/hadoop-streaming-*.jar  -input /tmp/xxx -output /tmp/yyy -mapper "python test.py"  -file test.py
```
2.直接使用shell命令
```
hadoop  jar <hadoop_home>/share/hadoop/tools/lib/hadoop-streaming-2.3.0-cdh5.0.0.jar  -input /tmp/xxx -output /tmp/yyy -mapper cat -reducer "wc -l" 
```
  

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
   hadoop使用crc-32进行数据完整性检查。
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
##mapreduce计数器
用来观察job运行期的各种细节数据。
mapreduce自带的counter含义。
MapReduce job提供的默认Counter分为五个组
###File Input Format Counters 
    1. BYTES_READ 
             Map task的所有输入数据(字节)，等于各个map task的map方法传入的所有value值字节之和。
         
###File System Counters 
1. FILE_BYTES_READ	
        job读取本地文件系统的文件字节数。假定我们当前map的输入数据都来自于HDFS，那么在map阶段，这个数据应该是0。但reduce在执行前，它的输入数据是经过shuffle的merge后存储在reduce端本地磁盘中，所以这个数据就是所有reduce的总输入字节数。

2. FILE_BYTES_WRITTEN 
        map的中间结果都会spill到本地磁盘中，在map执行完后，形成最终的spill文件。所以map端这里的数据就表示map task往本地磁盘中总共写了多少字节。与map端相对应的是，reduce端在shuffle时，会不断地拉取map端的中间结果，然后做merge并不断spill到自己的本地磁盘中。最终形成一个单独文件，这个文件就是reduce的输入文件。 

3. HDFS_BYTES_READ 
        整个job执行过程中，只有map端运行时，才从HDFS读取数据，这些数据不限于源文件内容，还包括所有map的split元数据。所以这个值应该比FileInputFormatCounters.BYTES_READ 要略大些。 

4. HDFS_BYTES_WRITTEN 
        Reduce的最终结果都会写入HDFS，就是一个job执行结果的总量。

###Shuffle Errors 
   这组内描述Shuffle过程中的各种错误情况发生次数。 

###Job Counters 
1. all map tasks (ms) 
        所有map task占用时间 
2. all reduce tasks (ms)
        与上面类似 
3. all maps in occupied slots(ms)
        所有map task占用slot的总时间，包含执行时间和创建/销毁子JVM的时间 
4. all reduces in occupied slots(ms)
        与上面类似 
5. Launched map tasks 
        此job启动了多少个map task 
6. Launched reduce tasks 
        此job启动了多少个reduce task 
7. Rack-local map tasks
        本地机架上的map task数量

###Map-Reduce Framework 
1. Combine input records 
        Combiner是为了减少尽量减少需要拉取和移动的数据，所以combine输入条数与map的输出条数是一致的。 

2. Combine output records 
        经过Combiner后，相同key的数据经过压缩，在map端自己解决了很多重复数据，表示最终在map端中间文件中的所有条目数 

3. Failed Shuffles 
        copy线程在抓取map端中间数据时，如果因为网络连接异常或是IO异常，所引起的shuffle错误次数 

4. GC time elapsed(ms) 
        通过JMX获取到执行map与reduce的子JVM总共的GC时间消耗 

5. Map input records 
        所有map task从HDFS读取的文件总行数 

6. Map output records 
        map task的直接输出record是多少，就是在map方法中调用context.write的次数，也就是未经过Combine时的原生输出条数 

7. Map output bytes 
        Map的输出结果key/value都会被序列化到内存缓冲区中，所以这里的bytes指序列化后的最终字节之和 
8. Map output materialized bytes
        Map最终写入磁盘的字节之和

9. Merged Map outputs 
        记录着shuffle过程中总共经历了多少次merge动作 

10. Reduce input groups 
        Reduce总共读取了多少个这样的groups 

11. Reduce input records 
        如果有Combiner的话，那么这里的数值就等于map端Combiner运算后的最后条数，如果没有，那么就应该等于map的输出条数 

12. Reduce output records 
        所有reduce执行后输出的总条目数 

13. Reduce shuffle bytes 
        Reduce端的copy线程总共从map端抓取了多少的中间数据，表示各个map task最终的中间文件总和 

14. Shuffled Maps 
         每个reduce几乎都得从所有map端拉取数据，每个copy线程拉取成功一个map的数据，那么增1，所以它的总数基本等于 reduce number * map number 

15. Spilled Records 
        spill过程在map和reduce端都会发生，这里统计在总共从内存往磁盘中spill了多少条数据 

16. SPLIT_RAW_BYTES 
        与map task 的split相关的数据都会保存于HDFS中，而在保存时元数据也相应地存储着数据是以怎样的压缩方式放入的，它的具体类型是什么，这些额外的数据是MapReduce框架加入的，与job无关，这里记录的大小就是表示额外信息的字节大小 


##hadoop自定义计数器

http://my.oschina.net/leejun2005/blog/276891

