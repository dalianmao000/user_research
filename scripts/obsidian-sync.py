#!/usr/bin/env python3
"""
Obsidian Sync Tool - User Research AI Agents
同步用户研究笔记到 Obsidian 知识库
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import hashlib


class ObsidianSync:
    """Obsidian 知识库同步工具"""

    def __init__(self, vault_path: str = "./obsidian-vault"):
        self.vault_path = Path(vault_path)
        self.config_file = self.vault_path / ".obsidian-sync.json"
        self.notes_dir = self.vault_path / "notes"
        self.archives_dir = self.vault_path / "archives"
        self.index_file = self.vault_path / "index.json"

        self.config = self._load_config()
        self.index = self._load_index()

    def _load_config(self) -> Dict:
        """加载配置文件"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "last_sync": None,
            "sync_history": []
        }

    def _save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def _load_index(self) -> Dict:
        """加载笔记索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "notes": {},
            "tags": {},
            "last_updated": None
        }

    def _save_index(self):
        """保存笔记索引"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def _compute_hash(self, content: str) -> str:
        """计算内容哈希"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]

    def _ensure_dirs(self):
        """确保必要目录存在"""
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        self.archives_dir.mkdir(parents=True, exist_ok=True)

    def init(self) -> bool:
        """初始化 Obsidian Vault"""
        try:
            self._ensure_dirs()

            # 创建目录结构
            (self.vault_path / "daily").mkdir(exist_ok=True)
            (self.vault_path / "interviews").mkdir(exist_ok=True)
            (self.vault_path / "insights").mkdir(exist_ok=True)
            (self.vault_path / "requirements").mkdir(exist_ok=True)
            (self.vault_path / "reports").mkdir(exist_ok=True)
            (self.vault_path / "templates").mkdir(exist_ok=True)

            # 创建模板文件
            self._create_templates()

            self.config["last_sync"] = datetime.now().isoformat()
            self._save_config()
            self._save_index()

            print(f"Obsidian Vault 初始化完成: {self.vault_path}")
            return True

        except Exception as e:
            print(f"初始化失败: {e}")
            return False

    def _create_templates(self):
        """创建笔记模板"""
        templates = {
            "interview-template.md": """# 访谈记录

- 日期: {{date}}
- 受访者: {{interviewee}}
- 角色: {{role}}
- 访谈时长: {{duration}}

## 基本信息
- 行业:
- 经验年限:
- 公司规模:

## 访谈内容

### 背景介绍


### 主题1


### 主题2


## 关键洞察
- 痛点:
- 期望:
- 行为:
- 建议:

## 后续行动
- [ ]
""",
            "insight-template.md": """# 用户洞察

- 创建日期: {{date}}
- 来源: {{source}}
- 类型: {{type}}

## 洞察描述

## 证据
> "引用内容"

## 影响分析
- 影响范围:
- 影响程度:
- 优先级:

## 关联洞察


## 行动项
- [ ]
""",
            "requirement-template.md": """---
需求ID: {{id}}
标题: {{title}}
优先级: {{priority}}
状态: 草稿
创建日期: {{date}}
---

# {{title}}

## 概述


## 用户故事
作为 [角色]，我希望 [功能]，以便 [收益]。

## 详细描述

### 背景


### 功能详情


### 验收标准
- [ ]

## 关联需求


## 评审记录
| 日期 | 评审人 | 意见 |
|-----|-------|-----|
"""
        }

        for filename, content in templates.items():
            template_path = self.vault_path / "templates" / filename
            if not template_path.exists():
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write(content)

    def add_note(self, note_type: str, content: str, metadata: Optional[Dict] = None) -> str:
        """添加笔记"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        note_hash = self._compute_hash(content)
        filename = f"{timestamp}-{note_hash}.md"

        type_dirs = {
            "interview": "interviews",
            "insight": "insights",
            "requirement": "requirements",
            "report": "reports"
        }

        target_dir = self.notes_dir / type_dirs.get(note_type, "notes")
        target_dir.mkdir(parents=True, exist_ok=True)

        note_path = target_dir / filename

        # 添加元数据头
        frontmatter = f"""---
created: {datetime.now().isoformat()}
type: {note_type}
hash: {note_hash}
"""

        if metadata:
            for key, value in metadata.items():
                frontmatter += f"{key}: {value}\n"

        frontmatter += "---\n\n"

        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)

        # 更新索引
        self._update_index(note_type, str(note_path), metadata or {})

        print(f"笔记已添加: {note_path}")
        return str(note_path)

    def _update_index(self, note_type: str, note_path: str, metadata: Dict):
        """更新笔记索引"""
        note_id = str(Path(note_path).stem)

        self.index["notes"][note_id] = {
            "path": note_path,
            "type": note_type,
            "metadata": metadata,
            "indexed_at": datetime.now().isoformat()
        }

        # 更新标签索引
        if "tags" in metadata:
            for tag in metadata.get("tags", []):
                if tag not in self.index["tags"]:
                    self.index["tags"][tag] = []
                self.index["tags"][tag].append(note_id)

        self._save_index()

    def sync(self, source_path: str, note_type: str = "notes") -> int:
        """同步外部笔记到 Obsidian"""
        source = Path(source_path)
        if not source.exists():
            print(f"源路径不存在: {source_path}")
            return 0

        count = 0
        if source.is_file():
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
            self.add_note(note_type, content)
            count = 1
        else:
            for file in source.rglob("*.md"):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.add_note(note_type, content)
                count += 1

        self.config["last_sync"] = datetime.now().isoformat()
        self.config["sync_history"].append({
            "time": datetime.now().isoformat(),
            "source": source_path,
            "count": count
        })
        self._save_config()

        print(f"同步完成: {count} 个文件")
        return count

    def archive_note(self, note_id: str) -> bool:
        """归档笔记"""
        for note_data in self.index["notes"].values():
            if note_data["path"].endswith(note_id):
                note_path = Path(note_data["path"])
                if note_path.exists():
                    archive_path = self.archives_dir / note_path.name
                    shutil.move(str(note_path), str(archive_path))
                    print(f"笔记已归档: {archive_path}")
                    return True
        return False

    def search_notes(self, query: str) -> List[Dict]:
        """搜索笔记"""
        results = []
        query_lower = query.lower()

        for note_id, note_data in self.index["notes"].items():
            path = Path(note_data["path"])
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if query_lower in content.lower():
                    results.append({
                        "id": note_id,
                        "path": str(path),
                        "type": note_data["type"],
                        "metadata": note_data["metadata"]
                    })

        return results

    def export_index(self, output_path: str = "index.json") -> bool:
        """导出索引"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, ensure_ascii=False)
            print(f"索引已导出: {output_path}")
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False

    def generate_daily_note(self) -> str:
        """生成每日笔记"""
        today = datetime.now()
        date_str = today.strftime("%Y-%m-%d")
        daily_path = self.vault_path / "daily" / f"{date_str}.md"

        if daily_path.exists():
            return str(daily_path)

        content = f"""# {date_str}

## 今日计划

## 访谈记录


## 洞察


## 行动项
- [ ]

## 备注

"""

        with open(daily_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"每日笔记已创建: {daily_path}")
        return str(daily_path)

    def backup(self, backup_dir: str = "./backups") -> str:
        """备份知识库"""
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"obsidian-backup-{timestamp}"
        backup_full = backup_path / backup_name

        shutil.copytree(self.vault_path, backup_full, dirs_exist_ok=True)

        print(f"备份已创建: {backup_full}")
        return str(backup_full)


def main():
    parser = argparse.ArgumentParser(description="Obsidian Sync Tool")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init 命令
    subparsers.add_parser("init", help="初始化 Obsidian Vault")

    # add 命令
    add_parser = subparsers.add_parser("add", help="添加笔记")
    add_parser.add_argument("type", choices=["interview", "insight", "requirement", "report"], help="笔记类型")
    add_parser.add_argument("-c", "--content", required=True, help="笔记内容")
    add_parser.add_argument("-m", "--metadata", help="元数据 (JSON格式)")

    # sync 命令
    sync_parser = subparsers.add_parser("sync", help="同步笔记")
    sync_parser.add_argument("source", help="源路径")
    sync_parser.add_argument("-t", "--type", default="notes", help="笔记类型")

    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索笔记")
    search_parser.add_argument("query", help="搜索关键词")

    # export 命令
    export_parser = subparsers.add_parser("export", help="导出索引")
    export_parser.add_argument("-o", "--output", default="index.json", help="输出文件")

    # daily 命令
    subparsers.add_parser("daily", help="生成每日笔记")

    # backup 命令
    backup_parser = subparsers.add_parser("backup", help="备份知识库")
    backup_parser.add_argument("-d", "--dir", default="./backups", help="备份目录")

    args = parser.parse_args()

    vault_path = os.environ.get("OBSIDIAN_VAULT_PATH", "./obsidian-vault")
    sync = ObsidianSync(vault_path)

    if args.command == "init":
        sync.init()
    elif args.command == "add":
        metadata = {}
        if args.metadata:
            metadata = json.loads(args.metadata)
        sync.add_note(args.type, args.content, metadata)
    elif args.command == "sync":
        sync.sync(args.source, args.type)
    elif args.command == "search":
        results = sync.search_notes(args.query)
        print(f"找到 {len(results)} 条结果:")
        for r in results:
            print(f"  - {r['path']} ({r['type']})")
    elif args.command == "export":
        sync.export_index(args.output)
    elif args.command == "daily":
        sync.generate_daily_note()
    elif args.command == "backup":
        sync.backup(args.dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()