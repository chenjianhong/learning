
#hdfs简要教程

##数据块
  hdfs默认的数据块大小为64MB或者128MB。
  主要是为了最小化寻址开销。
  磁盘驱动器传输速率提升，块的大小将更大。
  mapreduce中的map任务通常一次处理一个块，所以不能太大。
  
##hdfs中的文件访问权限
3种权限模式：读，写，执行（访问目录子项时需要）
每个文件和目录都有所属用户、所属类别及模式，模式是用户权限、组内权限，其他用户权限组成。

##hdfs文件操作
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
