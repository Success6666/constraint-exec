用 UTF-8 编码保存 JSON 文件，启动时读取即可：

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


# 简单用法：启动时恢复，修改后保存
todos = load_todos()
todos.append({"内容": "买牛奶", "完成": False})
save_todos(todos)

print(todos)
```

数据保存在当前工作目录的 `todos.json`，下次从同一目录启动即可恢复。
