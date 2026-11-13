用 UTF-8 编码读写 JSON 文件即可：

```python
import json
from pathlib import Path

TODO_FILE = Path("todos.json")


def load_todos():
    if not TODO_FILE.exists():
        return []
    return json.loads(TODO_FILE.read_text(encoding="utf-8"))


def save_todos(todos):
    TODO_FILE.write_text(
        json.dumps(todos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# 启动时恢复已有待办
todos = load_todos()

# 添加中文待办并保存
todos.append({"title": "买牛奶", "done": False})
save_todos(todos)

print(todos)
```

重启后调用 `load_todos()` 即可恢复。`todos.json` 保存在当前工作目录，`ensure_ascii=False` 让文件直接显示中文。
