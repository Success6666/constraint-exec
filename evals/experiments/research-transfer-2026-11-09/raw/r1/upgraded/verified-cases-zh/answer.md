12项单测全部通过，已验证：
- 中文 JSON 可正确回读。
- 文件缺失时返回 `[]`。
- JSON 格式错误时抛出 `ValueError`。
- 保留 `SENTINEL`。
