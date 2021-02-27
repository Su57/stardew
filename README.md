# 演示方法
安装poetry（项目使用poetry作为依赖管理。关于poetry，请参考 [poetry官方文档](https://python-poetry.org/docs/)）:
```
pip install poetry
```

将代码克隆到本地:
```
git clone https://github.com/Su57/stardew.git
```
安装依赖:

```
cd stardew
poetry install
```

在项目根目录下创建 .env 文件，并在其中设置如下变量(也可以直接设定系统环境变量)：
```
# 项目基本配置
SECRET_KEY # 密钥
PROJECT_NAME # 项目名

# 数据库连接配置
POSTGRES_HOST # pgsql host
POSTGRES_PORT
POSTGRES_NAME
POSTGRES_USER
POSTGRES_PASSWORD


# email配置
SMTP_TLS # 是否启用 TSL
SMTP_PORT # 邮件端口（开启TSL时，163邮箱默认为465）
SMTP_HOST # 邮件发件服务器（163邮箱为smtp.163.com）
SMTP_USER # 你的邮箱登录名
SMTP_LICENCE # 邮件授权码。获取方式参考 https://qiye.163.com/help/af988e.html
EMAIL_SENDER # 你的邮箱地址
EMAIL_FROM_NAME # 发件人名称

# redis配置
REDIS_NAME
REDIS_HOST
REDIS_PORT
REDIS_MAX_CONNECTIONS


# jwt配置
JWT_PREFIX
JWT_EXPIRED_MINUTES

# 日志配置。参考https://loguru.readthedocs.io/en/stable/overview.html
LOG_LEVEL
LOG_FORMAT
LOG_ROTATION

#验证码配置
CAPTCHA_CHAR_LENGTH # 验证码内容字符串长度。4或6即可
CAPTCHA_EXPIRED_MINUTES # 验证码有效期
```

执行数据库迁移命令

```
alembic upgrade head
```

启动服务
```
cd stardew
python runserver.py
```