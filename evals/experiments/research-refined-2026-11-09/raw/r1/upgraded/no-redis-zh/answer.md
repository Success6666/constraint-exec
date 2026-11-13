用 UTF-8 编码和 `ensure_ascii=False` 保存中文；文件不存在时返回空列表。

```python
import json
from pathlib import Path


def load_todos(filename="todos.json"):
    path = Path(filename)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_todos(todos, filename="todos.json"):
    Path(filename).write_text(
        json.dumps(todos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# 简单用法
todos = load_todos()  # 重启后从文件恢复
todos.append({"title": "买牛奶", "done": False})
save_todos(todos)
print(todos)
```

默认保存到当前工作目录的 `todos.json`；重启后使用同一路径即可恢复。
