用 UTF-8 编码读写 JSON 文件即可，文件不存在时返回空列表。

```python
import json
from pathlib import Path

TODO_FILE = Path("todos.json")


def load_todos():
    if not TODO_FILE.exists():
        return []
    with TODO_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_todos(todos):
    with TODO_FILE.open("w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


# 简单用法：启动时读取，修改后保存
todos = load_todos()
todos.append({"内容": "买牛奶", "完成": False})
save_todos(todos)

print(todos)
```

`ensure_ascii=False` 让文件直接保留中文。重启后调用 `load_todos()`，即可恢复已保存的待办；运行时保持同一工作目录。
