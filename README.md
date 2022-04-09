# 浙师大战役通自动签到

去tm的形式主义

方法1 : docker部署
```bash
docker run --shm-size=1g -v ~/zyt-auto-report:/root/config -d smalldecline/zyt-auto-report bash -c "cd /root && python3 Report.py"
```

用户配置文件在用户目录的zyt-auto-report文件夹里

方法2 : 自己搭建环境运行

相信聪明的你一定懂吧!