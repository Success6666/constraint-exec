已仅修改 `app.py`，保留 `SENTINEL`：

- 使用 UTF-8 JSON 保存，自动创建父目录
- 文件缺失返回空列表
- 无效 JSON 抛出 `ValueError`
- 中文待办可完整保存并恢复

已运行检查，4 项测试全部通过。
