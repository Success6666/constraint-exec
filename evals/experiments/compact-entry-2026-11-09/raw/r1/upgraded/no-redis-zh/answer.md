用 UTF-8 编码的 JSON 文件保存，启动时读取即可。文件不存在时返回空列表。

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
print("已有待办：", todos)

# 新增并保存
todos.append({"title": "买牛奶", "done": False})
save_todos(todos)
```

下次在同一工作目录运行时，会恢复之前保存的中文待办。
