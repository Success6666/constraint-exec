使用 UTF-8 编码保存，`ensure_ascii=False` 让 JSON 文件直接显示中文。

```python
import json


def load_todos(path="todos.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_todos(todos, path="todos.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


# 启动时恢复待办；文件不存在则返回空列表
todos = load_todos()
print("当前待办：", todos)

# 添加待办并保存
todos.append("买牛奶")
save_todos(todos)
```

文件默认保存在当前工作目录的 `todos.json`。重启后，在同一目录运行 `load_todos()` 即可恢复。
