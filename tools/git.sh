#!/bin/sh
# 本容器的工作区文件系统不允许 git 写对象目录，故把 GIT_DIR 放在 /tmp
exec git --git-dir=/tmp/rl-git --work-tree="$(cd "$(dirname "$0")/.." && pwd)" "$@"
