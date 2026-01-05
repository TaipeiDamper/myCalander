"""
Todo List 應用程式 - 資料模型
版本: v1.0.0
建立日期: 2024-01-XX
"""

from datetime import datetime
from typing import Optional


class Todo:
    """Todo 任務類別"""
    
    def __init__(self, title: str, content: str = "", date: str = "", 
                 time: str = "", completed: bool = False, todo_id: Optional[str] = None):
        """
        初始化 Todo 任務
        
        Args:
            title: 任務標題（顯示在月曆上）
            content: 任務詳細內容
            date: 任務日期 (格式: YYYY-MM-DD)
            time: 任務時間 (格式: HH:MM)
            completed: 是否已完成
            todo_id: 唯一識別碼（如果為 None 則自動生成）
        """
        self.id = todo_id if todo_id else self._generate_id()
        self.title = title
        self.content = content
        self.date = date
        self.time = time
        self.completed = completed
        self.order = 0  # 用於拖曳排序
    
    @staticmethod
    def _generate_id() -> str:
        """生成唯一 ID"""
        return f"todo_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def to_dict(self) -> dict:
        """轉換為字典格式（用於 JSON 儲存）"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "date": self.date,
            "time": self.time,
            "completed": self.completed,
            "order": self.order
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Todo':
        """從字典建立 Todo 物件"""
        todo = cls(
            title=data.get("title", ""),
            content=data.get("content", ""),
            date=data.get("date", ""),
            time=data.get("time", ""),
            completed=data.get("completed", False),
            todo_id=data.get("id")
        )
        todo.order = data.get("order", 0)
        return todo
    
    def get_datetime(self) -> Optional[datetime]:
        """
        取得任務的日期時間物件（用於排序）
        如果日期或時間不完整，返回 None
        """
        if not self.date:
            return None
        
        try:
            date_str = self.date
            time_str = self.time if self.time else "00:00"
            datetime_str = f"{date_str} {time_str}"
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except (ValueError, AttributeError):
            return None
    
    def __lt__(self, other: 'Todo') -> bool:
        """用於排序：越接近完成時刻越前面"""
        if self.completed and not other.completed:
            return False
        if not self.completed and other.completed:
            return True
        
        self_dt = self.get_datetime()
        other_dt = other.get_datetime()
        
        if self_dt is None and other_dt is None:
            return self.order < other.order
        if self_dt is None:
            return False
        if other_dt is None:
            return True
        
        if self_dt == other_dt:
            return self.order < other.order
        
        return self_dt < other_dt
    
    def __repr__(self) -> str:
        return f"Todo(id={self.id}, title={self.title}, date={self.date}, time={self.time})"

