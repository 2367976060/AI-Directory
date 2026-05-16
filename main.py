#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI智能项目一键生成系统 - Android Version
Built with Kivy cross-platform framework
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.app import AIProjectGenerator

if __name__ == '__main__':
    AIProjectGenerator().run()
