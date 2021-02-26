# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/10 13:31
# @Description   : 日志组件
import os

from loguru import logger

from stardew.common.constants import Constant
from stardew.settings import settings

log_dir = os.path.join(settings.BASE_DIR, "logs")
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
logger.add(
    sink=os.path.join(log_dir, "stardew.log"),
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    rotation=settings.LOG_ROTATION,
    compression="zip",
    encoding=Constant.UTF8
)
