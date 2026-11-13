已仅修改 `app.py`，保留 `SENTINEL`：
- JSON 保存，自动创建父目录
- 文件缺失返回空列表
- 无效 JSON 抛出 `ValueError`
- UTF-8 编码，中文待办可完整恢复

已运行检查，4 项测试全部通过。
