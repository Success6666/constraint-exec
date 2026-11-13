用 UTF-8 JSON 文件保存，每次修改后写入，重启时读取即可。

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

# 添加并保存
todos.append({"title": "买牛奶", "done": False})
save_todos(todos)

print(todos)
```

`todos.json` 保存在当前工作目录；重启后使用同一目录运行，就会恢复已保存的待办。
