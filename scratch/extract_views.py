import json
import os

log_path = r"C:\Users\ASAHI\.gemini\antigravity-ide\brain\4c70f361-ddc2-4366-bf46-5d2ced6e799e\.system_generated\logs\transcript.jsonl"

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
            source = obj.get("source")
            step_type = obj.get("type")
            content = obj.get("content", "")
            
            # 尋找由 SYSTEM 或 MODEL 發出的 VIEW_FILE 動作
            if step_type == "VIEW_FILE" and content:
                # 檢查路徑
                if "data_manager.py" in content:
                    lines = content.split("\n")
                    print(f"Found VIEW_FILE data_manager.py in step {obj.get('step_index')}, lines: {len(lines)}")
                    # 寫入備份
                    with open(f"C:\\Users\\ASAHI\\Desktop\\Personal_Research\\dylan_otherCode\\calander\\scratch\\dm_step_{obj.get('step_index')}.py", "w", encoding="utf-8") as out:
                        out.write(content)
                elif "stock_widget.py" in content:
                    lines = content.split("\n")
                    print(f"Found VIEW_FILE stock_widget.py in step {obj.get('step_index')}, lines: {len(lines)}")
                    with open(f"C:\\Users\\ASAHI\\Desktop\\Personal_Research\\dylan_otherCode\\calander\\scratch\\sw_step_{obj.get('step_index')}.py", "w", encoding="utf-8") as out:
                        out.write(content)
        except Exception as e:
            pass
print("Scan done!")
