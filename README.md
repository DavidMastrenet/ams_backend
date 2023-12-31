# 校园活动管理系统（后端）

上海师范大学 2023级计算机科学与技术（师范）

开发： 洪宇轩

面向对象程序设计、后端三层架构实践

## 文件说明

app.py -- 主程序

app/ -- 程序目录

### app目录

- config.py -- 配置文件
- models.py -- 数据库模型
- auth/ -- 权限认证模块
- controller/ -- API接口模块
- service/ -- 业务逻辑模块
- dao/ -- 数据库操作模块
- templates/ -- 前端目录 （由温志宏负责）

## 数据库

数据库结构见`sqlStruct.sql`

使用MySQL数据库，请自行修改`app/config.py`中的数据库配置

## 运行

安装依赖

```bash
pip install -r requirements.txt
```

修改`app/config.py`中的数据库、密钥配置后，运行以下命令即可启动服务

```bash
python app.py
```
