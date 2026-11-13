用 UTF-8 编码的 JSON 文件保存，重启后读取同一个文件即可恢复：

```python
import json
from pathlib import Path

FILE = Path("todos.json")


def load_todos():
    if not FILE.exists():
        return []
    with FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_todos(todos):
    with FILE.open("w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)
```

简单用法：

```python
todos = load_todos()
todos.append({"title": "买牛奶", "done": False})
save_todos(todos)

# 下次启动时读取
todos = load_todos()
print(todos)
```

`todos.json` 保存在当前工作目录；每次修改后调用 `save_todos()`。
