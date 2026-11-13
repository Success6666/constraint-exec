用 UTF-8 编码的 JSON 文件保存，重启后读取即可。文件不存在时返回空列表。

```python
import json
from pathlib import Path

FILE = Path("todos.json")


def save_todos(todos):
    FILE.write_text(
        json.dumps(todos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_todos():
    if not FILE.exists():
        return []
    return json.loads(FILE.read_text(encoding="utf-8"))


# 简单用法
todos = load_todos()
todos.append({"内容": "买牛奶", "完成": False})
save_todos(todos)

# 重启后也能恢复
print(load_todos())
```

`todos.json` 保存在当前工作目录；每次修改待办后调用 `save_todos()`。
