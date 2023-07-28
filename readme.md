# MPWA UnionBan

这是MPWA联合封禁插件的MCDR版本。

## 注意

这指是一个测试版本，大多数功能仍未实现。

## 安装

1.  从 [GitHub Releases](https://github.com/Minecraft-Public-Welfare-Alliance/UnionBan-MCDR/releases)下载最新版本的插件。
3.  重启服务器。

## 配置

该插件需要一个 MySQL 数据库来存储封禁数据。您需要在配置文件中提供以下配置：
```
MPWAUnionBan:
  mysql_host: localhost
  mysql_user: root
  mysql_password: password
  mysql_database: database
  check_interval: 3600
```

-   `mysql_host`：MySQL 服务器 IP 地址。
-   `mysql_user`：MySQL 服务器的用户名。
-   `mysql_password`：MySQL 服务器的密码。
-   `mysql_database`：MySQL 数据库名称。
-   `check_interval`：检查封禁列表的间隔（以秒为单位）。

## 命令

-   `!!uban <playerID> <Reason> <Reason_Text> <isOnline> <from>` 
对具有指定详细信息的玩家进行封禁。`<playerID>` 是要封禁的玩家的 ID，`<Reason>` 是封禁的原因（选项：hacking、stealing、destroying、other），`<Reason_Text>` 是关于封禁的详细信息，`<isOnline>` 是一个布尔值，表示玩家当前是否是在线玩家（正版），`from`是服务器名。
例子：`!!uban IamHackerTest hacking "开自动挖矿" true`
-   `!!reload` 
重新加载插件配置。

## 贡献者

-   [BaimoQilin](https://github.com/Zhou-Shilin) (Zhou-Shilin, from [Hypiworld](https://baimoqilin.top/hypiworld))

## TODO
- [x] 根据数据库封禁玩家
- [x] uban指令云封禁玩家
- [ ] 通过配置文件配置`!!uban`的`From`参数 
- [ ] 支持导入banlist
- [ ] 支持配置按照封禁原因封禁玩家
