#!/usr/bin/env bash
redis-server &
python proxyPool.py server &
python proxyPool.py schedule
