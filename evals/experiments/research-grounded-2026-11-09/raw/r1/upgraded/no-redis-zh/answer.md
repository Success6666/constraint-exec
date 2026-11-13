用 UTF-8 编码保存 JSON，`ensure_ascii=False` 让中文直接可读。文件不存在时返回空列表。

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


# 读取已有待办
todos = load_todos()

# 添加并保存
todos.append({"title": "买牛奶", "done": False})
save_todos(todos)

# 重启程序后，再次调用 load_todos() 即可恢复
print(load_todos())
```

默认文件位于当前工作目录；重启后使用同一路径即可。
