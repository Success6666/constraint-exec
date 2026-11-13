用 UTF-8 编码读写 JSON 文件即可：

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

# 简单用法
todos = load_todos()
todos.append({"内容": "买牛奶", "完成": False})
save_todos(todos)

# 重启后，在同一目录运行即可恢复
todos = load_todos()
print(todos)
```

`ensure_ascii=False` 让文件中的中文直接可读。
