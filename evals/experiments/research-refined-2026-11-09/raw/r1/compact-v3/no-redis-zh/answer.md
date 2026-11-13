用 UTF-8 编码和 `ensure_ascii=False` 保存中文，每次启动时读取文件即可恢复。

```python
import json
from pathlib import Path


def load_todos(filename="todos.json"):
    path = Path(filename)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_todos(todos, filename="todos.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)
```

简单用法：

```python
# 启动时恢复
todos = load_todos()

# 添加并保存
todos.append({"title": "买牛奶", "done": False})
save_todos(todos)

# 重启后再次读取，数据仍在
print(load_todos())
```

默认文件为当前工作目录下的 `todos.json`；重启时使用同一路径即可。
