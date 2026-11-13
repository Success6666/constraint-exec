用 UTF-8 编码保存 JSON，程序启动时读取即可恢复：

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

# 启动时恢复
todos = load_todos()

# 添加并保存
todos.append({"内容": "买牛奶", "完成": False})
save_todos(todos)

print(todos)
```

重启后调用 `load_todos()` 就能恢复已保存的待办。默认文件位于当前工作目录，再次启动时保持该目录一致即可。
