# 工具函数，可用于后续扩展

def safe_write(path, content):
    from pathlib import Path
    Path(path).write_text(content, encoding='utf-8')
