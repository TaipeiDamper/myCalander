"""
Todo List 應用程式 - 資料管理
版本: v1.0.0
建立日期: 2024-01-XX
"""

import json
import os
from typing import List
from core.models import Todo


import sys
def get_data_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(get_data_path(), "todos.json")


def load_todos() -> List[Todo]:
    """
    從 JSON 檔案載入所有 todo
    
    Returns:
        Todo 物件列表
    """
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            todos_data = data.get("todos", [])
            return [Todo.from_dict(todo_data) for todo_data in todos_data]
    except (json.JSONDecodeError, IOError) as e:
        print(f"載入資料時發生錯誤: {e}")
        return []


def save_todos(todos: List[Todo]) -> bool:
    """
    儲存所有 todo 到 JSON 檔案
    
    Args:
        todos: Todo 物件列表
    
    Returns:
        是否成功儲存
    """
    try:
        data = {
            "todos": [todo.to_dict() for todo in todos]
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"儲存資料時發生錯誤: {e}")
        return False


def get_todos_by_date(todos: List[Todo], date: str) -> List[Todo]:
    """
    取得指定日期的所有 todo
    
    Args:
        todos: 所有 todo 列表
        date: 日期字串 (格式: YYYY-MM-DD)
    
    Returns:
        該日期的 todo 列表
    """
    return [todo for todo in todos if todo.date == date]


def get_incomplete_todos(todos: List[Todo]) -> List[Todo]:
    """
    取得所有未完成的 todo
    
    Args:
        todos: 所有 todo 列表
    
    Returns:
        未完成的 todo 列表（已排序）
    """
    incomplete = [todo for todo in todos if not todo.completed]
    return sorted(incomplete)


