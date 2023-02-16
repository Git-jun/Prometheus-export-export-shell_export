# 自定义一个Prometheus的export监控
## 由于Prometheus的本身的export监控有很多监控项是我们并不关心的，在我们实际的生产环境中我们往往需要定制自己的监控项 于是就有了我这个项目

本项目只需要在 ./config/export.yaml 配置上自己需要监控项的名字以及对应获取值的命令然后运行项目就可以实现定制化的监控
config/export.yaml文件的例子如下
```yaml
monitoring:
  - name: TCP_ESTABLISHED 
    help: "Monitoring tcp connection status belongs to ESTABLISHED"
    command: "netstat -ant |grep 80|grep ESTABLISHED|wc -l"
    interval: 30s

```

* 运行项目确保有python3环境具体版本没有特殊要求
* 安装依赖
```
pip3 install prometheus_client
```
* 修改export.yaml文件按照上述例子修改
* 运行项目 
```
nohup python3 shell_export.py &
```
