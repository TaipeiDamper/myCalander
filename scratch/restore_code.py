import json
import os

log_path = r"C:\Users\ASAHI\.gemini\antigravity-ide\brain\4c70f361-ddc2-4366-bf46-5d2ced6e799e\.system_generated\logs\transcript.jsonl"

dm_path = r"c:\Users\ASAHI\Desktop\Personal_Research\dylan_otherCode\calander\stock\data_manager.py"
sw_path = r"c:\Users\ASAHI\Desktop\Personal_Research\dylan_otherCode\calander\stock\stock_widget.py"

# 重置檔案回 git 乾淨的狀態（即最原始的狀態），防止重複執行導致出錯
# 因為工作目錄是 clean 的，所以我們可以直接從 git checkout 還原
os.system(f"git checkout -- \"{dm_path}\"")
os.system(f"git checkout -- \"{sw_path}\"")

with open(dm_path, "r", encoding="utf-8") as f:
    dm_content = f.read()

with open(sw_path, "r", encoding="utf-8") as f:
    sw_content = f.read()

print("Original data_manager.py length:", len(dm_content))
print("Original stock_widget.py length:", len(sw_content))

def ensure_json_parsed(val):
    if isinstance(val, str):
        # 移除外層可能的引號
        val_strip = val.strip()
        if (val_strip.startswith('"') and val_strip.endswith('"')) or \
           (val_strip.startswith('[') and val_strip.endswith(']')) or \
           (val_strip.startswith('{') and val_strip.endswith('}')):
            try:
                parsed = json.loads(val_strip)
                if parsed != val:
                    return ensure_json_parsed(parsed)
            except:
                pass
    return val

def apply_replace(content, target, replacement):
    target = ensure_json_parsed(target)
    replacement = ensure_json_parsed(replacement)
    
    # 統一換行符為 \n
    c_norm = content.replace("\r\n", "\n")
    t_norm = target.replace("\r\n", "\n")
    r_norm = replacement.replace("\r\n", "\n")
    
    if t_norm not in c_norm:
        t_strip = t_norm.strip()
        if t_strip in c_norm:
            idx = c_norm.find(t_strip)
            c_norm = c_norm[:idx] + r_norm + c_norm[idx + len(t_strip):]
            print("  Partial strip match applied successfully.")
            return c_norm
        print("  WARNING: TargetContent not found in content!")
        print("  Target tried (first 100 chars):", repr(t_norm[:100]))
        return content
    
    c_norm = c_norm.replace(t_norm, r_norm, 1)
    print("  Replacement applied successfully.")
    return c_norm

# 讀取 steps
steps = []
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            steps.append(json.loads(line))
        except Exception as e:
            pass

steps.sort(key=lambda x: x.get("step_index", 0))

for step in steps:
    tool_calls = step.get("tool_calls", [])
    if not tool_calls:
        continue
        
    for tc in tool_calls:
        func = tc.get("name")
        args = tc.get("args", {})
        
        target_file = args.get("TargetFile", "")
        target_file = ensure_json_parsed(target_file)
        
        if not target_file:
            continue
            
        is_dm = "data_manager.py" in target_file
        is_sw = "stock_widget.py" in target_file
        
        if not (is_dm or is_sw):
            continue
            
        print(f"Replaying step {step.get('step_index')}: {func} on {os.path.basename(target_file)}")
        
        current_content = dm_content if is_dm else sw_content
        
        if func == "write_to_file":
            code_content = ensure_json_parsed(args.get("CodeContent", ""))
            current_content = code_content
            print("  File fully overwritten via write_to_file.")
            
        elif func == "replace_file_content":
            target = args.get("TargetContent", "")
            rep = args.get("ReplacementContent", "")
            current_content = apply_replace(current_content, target, rep)
            
        elif func == "multi_replace_file_content":
            chunks = args.get("ReplacementChunks", [])
            chunks = ensure_json_parsed(chunks)
            for chunk in chunks:
                target = chunk.get("TargetContent", "")
                rep = chunk.get("ReplacementContent", "")
                current_content = apply_replace(current_content, target, rep)
                
        if is_dm:
            dm_content = current_content
        else:
            sw_content = current_content

# 寫回檔案
with open(dm_path, "w", encoding="utf-8", newline="\r\n") as f:
    f.write(dm_content.replace("\r\n", "\n").replace("\n", "\r\n"))

with open(sw_path, "w", encoding="utf-8", newline="\r\n") as f:
    f.write(sw_content.replace("\r\n", "\n").replace("\n", "\r\n"))

print("Restoration complete!")
print("Final data_manager.py length:", len(dm_content))
print("Final stock_widget.py length:", len(sw_content))
