用 UTF-8 编码读写 JSON 文件：

```python
import json
from pathlib import Path

FILE = Path("todos.json")


def load_todos():
    if not FILE.exists():
        return []
    return json.loads(FILE.read_text(encoding="utf-8"))


def save_todos(todos):
    FILE.write_text(
        json.dumps(todos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# 启动时恢复
todos = load_todos()

# 添加中文待办并保存
todos.append({"内容": "买牛奶", "完成": False})
save_todos(todos)

print(todos)
```

待办保存在当前工作目录的 `todos.json` 中；重启后在同一目录运行即可读取。
