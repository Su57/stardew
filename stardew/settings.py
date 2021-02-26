# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/12 12:46
# @Description   :
import os
import secrets
from typing import Any, Dict, Optional

from pydantic import BaseSettings, EmailStr, PostgresDsn, RedisDsn, validator

BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))


class Settings(BaseSettings):
    """
    配置解析。参考 https://pydantic-docs.helpmanual.io/usage/settings/
    优先级: 直接指定的值 > 环境变量 > .env文件 > secrets目录 > 默认值
    """
    # 项目基本配置
    BASE_DIR: str = BASE_DIR
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str

    # 数据库连接配置
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            host=values.get("POSTGRES_HOST"),
            port=f"{values.get('POSTGRES_PORT')}",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            path=f"/{values.get('POSTGRES_NAME') or ''}",
        )

    # email配置
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_LICENCE: Optional[str] = None
    EMAIL_SENDER: Optional[EmailStr] = None
    EMAIL_FROM_NAME: Optional[str] = None

    # redis配置
    REDIS_HOST: str
    REDIS_NAME: Optional[str] = "0"
    REDIS_PORT: Optional[int] = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_MAX_CONNECTIONS: Optional[int] = 2000
    REDIS_DSN: Optional[RedisDsn] = None

    @validator("REDIS_DSN", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme='redis',
            host=values.get("REDIS_HOST"),
            port=f"{values.get('REDIS_PORT')}",
            password=values.get("REDIS_PASSWORD"),
            path=f"/{values.get('REDIS_NAME')}"
        )

    # jwt配置
    JWT_PREFIX: Optional[str] = "Bearer"
    JWT_EXPIRED_MINUTES: Optional[int] = 60

    # 日志配置
    LOG_LEVEL: Optional[int] = 0
    LOG_FORMAT: Optional[str] = None
    LOG_ROTATION: Optional[str] = "1 week"

    # 验证码配置
    CAPTCHA_CHAR_LENGTH: Optional[int] = 4
    CAPTCHA_EXPIRED_MINUTES: Optional[int] = 5

    class Config:
        case_sensitive = True
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = 'utf-8'


settings = Settings()


