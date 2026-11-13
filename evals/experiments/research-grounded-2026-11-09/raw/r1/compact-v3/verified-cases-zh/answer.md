12项单测全部通过，已验证：

- 中文 JSON 可正确回读。
- 文件缺失时返回 `[]`。
- JSON 格式损坏时抛出 `ValueError`。
- `SENTINEL` 得以保留。
