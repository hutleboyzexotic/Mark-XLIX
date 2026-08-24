"""
OpenClaw Skills Loader
Dynamically loads all SKILL.md files from the openclaw/skills directory
and converts them into tool declarations for Jarvis.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class SkillLoader:
    """Loads and parses OpenClaw SKILL.md files"""
    
    def __init__(self, skills_dir: str | Path = None):
        """
        Initialize the skill loader.
        
        Args:
            skills_dir: Path to the skills directory. Defaults to ../openclaw/skills
        """
        if skills_dir is None:
            # Default to ../openclaw/skills relative to this file
            current_dir = Path(__file__).parent
            skills_dir = current_dir.parent / "openclaw" / "skills"
        
        self.skills_dir = Path(skills_dir)
        self.skills: Dict[str, Dict[str, Any]] = {}
        self._load_all_skills()
    
    def _load_all_skills(self) -> None:
        """Load all SKILL.md files from the skills directory"""
        if not self.skills_dir.exists():
            print(f"⚠️  Skills directory not found: {self.skills_dir}")
            return
        
        skill_folders = [d for d in self.skills_dir.iterdir() if d.is_dir()]
        print(f"🔍 Found {len(skill_folders)} skill folders")
        
        for skill_folder in sorted(skill_folders):
            skill_md = skill_folder / "SKILL.md"
            if skill_md.exists():
                try:
                    skill_data = self._parse_skill_md(skill_md)
                    if skill_data:
                        self.skills[skill_folder.name] = skill_data
                        print(f"✅ Loaded skill: {skill_folder.name}")
                except Exception as e:
                    print(f"❌ Error loading {skill_folder.name}: {e}")
    
    def _parse_skill_md(self, md_path: Path) -> Optional[Dict[str, Any]]:
        """
        Parse a SKILL.md file and extract metadata.
        
        SKILL.md format:
        name: skill-name
        description: "Skill description"
        homepage: https://example.com
        metadata: {...}
        ---
        # Markdown documentation
        """
        content = md_path.read_text(encoding="utf-8")
        
        # Split frontmatter from body
        if "---" not in content:
            return None
        
        frontmatter_str, body = content.split("---", 1)
        
        # Parse YAML-like frontmatter
        skill_data = {}
        for line in frontmatter_str.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"')
                
                if key == "name":
                    skill_data["name"] = value
                elif key == "description":
                    skill_data["description"] = value
                elif key == "homepage":
                    skill_data["homepage"] = value
        
        # Extract first heading from body as fallback description
        if not skill_data.get("description"):
            match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            if match:
                skill_data["description"] = match.group(1)
        
        # Extract command examples from body
        examples = []
        for match in re.finditer(r"`([^`]+)`", body):
            cmd = match.group(1)
            if cmd.startswith(skill_data.get("name", "")):
                examples.append(cmd)
        
        if examples:
            skill_data["examples"] = examples[:3]  # Keep first 3 examples
        
        skill_data["body"] = body[:500]  # Store first 500 chars of body
        
        return skill_data if skill_data.get("name") else None
    
    def get_all_skills(self) -> Dict[str, Dict[str, Any]]:
        """Return all loaded skills"""
        return self.skills
    
    def get_skill(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific skill by name"""
        return self.skills.get(name)
    
    def get_skill_count(self) -> int:
        """Return total number of skills loaded"""
        return len(self.skills)
    
    def get_tool_declarations(self) -> List[Dict[str, Any]]:
        """
        Convert all skills to Jarvis TOOL_DECLARATIONS format.
        This allows Jarvis to recognize and call any skill.
        """
        tools = []
        
        for skill_name, skill_info in sorted(self.skills.items()):
            tool = {
                "name": skill_name.replace("-", "_"),
                "description": skill_info.get("description", f"OpenClaw skill: {skill_name}"),
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "command": {
                            "type": "STRING",
                            "description": f"Command to execute for {skill_name}"
                        },
                        "args": {
                            "type": "STRING",
                            "description": "Arguments for the command"
                        }
                    },
                    "required": ["command"]
                }
            }
            
            # Add examples to description if available
            if skill_info.get("examples"):
                examples_str = "\n".join(f"  - {ex}" for ex in skill_info["examples"][:2])
                tool["description"] += f"\n\nExamples:\n{examples_str}"
            
            tools.append(tool)
        
        return tools


class SkillExecutor:
    """Executes OpenClaw skills via CLI"""
    
    @staticmethod
    def execute_skill(skill_name: str, command: str, args: str = "") -> str:
        """
        Execute a skill command.
        
        Args:
            skill_name: Name of the skill (e.g., "gemini")
            command: Command to execute
            args: Optional arguments for the command
        
        Returns:
            Command output or error message
        """
        import subprocess
        import platform
        
        try:
            # Build the command
            full_command = f"{skill_name} {command}"
            if args:
                full_command += f" {args}"
            
            # Execute with timeout
            creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if platform.system() == "Windows" else 0
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=creationflags
            )
            
            if result.returncode == 0:
                return result.stdout.strip() or "Command executed successfully"
            else:
                return f"Error: {result.stderr.strip() or f'Exit code {result.returncode}'}"
        
        except subprocess.TimeoutExpired:
            return f"Skill execution timed out after 30 seconds"
        except Exception as e:
            return f"Failed to execute skill: {str(e)}"


def create_skill_tool_declarations() -> List[Dict[str, Any]]:
    """
    Create TOOL_DECLARATIONS for all OpenClaw skills.
    
    This function is called by main.py to add all skills to Jarvis.
    """
    try:
        loader = SkillLoader()
        count = loader.get_skill_count()
        print(f"🎯 Loaded {count} OpenClaw skills")
        
        tools = loader.get_tool_declarations()
        return tools
    
    except Exception as e:
        print(f"❌ Error creating skill tool declarations: {e}")
        return []


if __name__ == "__main__":
    # Test the skill loader
    loader = SkillLoader()
    print(f"\n📊 Skill Summary:")
    print(f"Total skills loaded: {loader.get_skill_count()}")
    print(f"\nSkill names:")
    for name in sorted(loader.get_all_skills().keys()):
        print(f"  - {name}")
    
    print(f"\nSample skill (gemini):")
    gemini = loader.get_skill("gemini")
    if gemini:
        print(f"  Name: {gemini.get('name')}")
        print(f"  Description: {gemini.get('description')}")
        print(f"  Homepage: {gemini.get('homepage')}")
