# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 12:05
# @Description   :
from enum import IntEnum


class StatusEnum(IntEnum):
    enable = 0
    disable = 1


class GenderEnum(IntEnum):
    """ 性别类型 0: 未知 1：男 2：女"""
    unknown = 0
    male = 1
    female = 2


class MenuTypeEnum(IntEnum):
    """ 按钮类型 0: 目录 1：菜单 2：按钮"""
    category = 0
    menu = 1
    button = 2
