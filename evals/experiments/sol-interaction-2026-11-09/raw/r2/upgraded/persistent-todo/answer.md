已仅修改 `app.py`，保留 `SENTINEL`：

- JSON 保存并自动创建父目录。
- 文件缺失返回空列表。
- 无效 JSON 抛出 `ValueError`。
- 使用 UTF-8，完整恢复中文待办。

已运行检查，4 项测试全部通过。
