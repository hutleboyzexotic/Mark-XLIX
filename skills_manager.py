"""
OpenClaw Skills Manager for Jarvis
Integrates all 51+ OpenClaw skills into the Jarvis action routing system.
"""

from typing import Any, Dict, List
from skills_loader import SkillLoader, SkillExecutor
import asyncio
import threading


class SkillsManager:
    """
    Manages OpenClaw skills integration with Jarvis.
    
    This class:
    1. Loads all SKILL.md files from openclaw/skills
    2. Creates tool declarations for Jarvis
    3. Routes skill calls to the skill executor
    4. Handles async/blocking execution
    """
    
    def __init__(self, skills_dir: str = None):
        """Initialize the skills manager"""
        self.loader = SkillLoader(skills_dir)
        self.executor = SkillExecutor()
        print(f"✅ Skills Manager initialized with {self.loader.get_skill_count()} skills")
    
    def get_tool_declarations(self) -> List[Dict[str, Any]]:
        """Get all skill tool declarations for Jarvis TOOL_DECLARATIONS"""
        return self.loader.get_tool_declarations()
    
    def handle_skill_call(self, skill_name: str, command: str, args: str = "") -> str:
        """
        Handle a skill execution call from Jarvis.
        
        Args:
            skill_name: Name of the skill to execute
            command: Command to run
            args: Optional arguments
        
        Returns:
            Execution result
        """
        # Normalize skill name (replace underscores with hyphens)
        normalized_name = skill_name.replace("_", "-")
        
        # Check if skill exists
        if normalized_name not in self.loader.get_all_skills():
            return f"❌ Skill '{skill_name}' not found. Available skills: {', '.join(sorted(self.loader.get_all_skills().keys())[:10])}..."
        
        # Execute the skill
        print(f"🚀 Executing skill: {normalized_name} {command}")
        result = self.executor.execute_skill(normalized_name, command, args)
        
        return result
    
    def list_skills(self) -> str:
        """Return a formatted list of all available skills"""
        skills = self.loader.get_all_skills()
        
        if not skills:
            return "❌ No skills loaded"
        
        output = f"📚 Available OpenClaw Skills ({len(skills)} total):\n\n"
        for name, info in sorted(skills.items()):
            desc = info.get("description", "No description")
            output += f"  • {name}\n"
            output += f"    {desc}\n"
        
        return output
    
    def get_skill_help(self, skill_name: str) -> str:
        """Get detailed help for a specific skill"""
        skill = self.loader.get_skill(skill_name)
        
        if not skill:
            return f"❌ Skill '{skill_name}' not found"
        
        output = f"📖 {skill_name} - OpenClaw Skill\n\n"
        output += f"Description: {skill.get('description', 'N/A')}\n"
        output += f"Homepage: {skill.get('homepage', 'N/A')}\n"
        
        if skill.get("examples"):
            output += f"\nExamples:\n"
            for example in skill["examples"]:
                output += f"  {example}\n"
        
        return output


# Global skills manager instance
_skills_manager = None


def get_skills_manager(skills_dir: str = None) -> SkillsManager:
    """Get or create the global skills manager"""
    global _skills_manager
    if _skills_manager is None:
        _skills_manager = SkillsManager(skills_dir)
    return _skills_manager


# Integration functions for main.py


def integrate_skills_into_jarvis() -> List[Dict[str, Any]]:
    """
    Called by main.py to integrate all OpenClaw skills into TOOL_DECLARATIONS.
    
    Returns:
        List of tool declarations for all skills
    """
    manager = get_skills_manager()
    tools = manager.get_tool_declarations()
    print(f"🎯 Added {len(tools)} OpenClaw skills to Jarvis")
    return tools


async def execute_skill_async(skill_name: str, command: str, args: str = "") -> str:
    """
    Async wrapper for skill execution.
    Runs in thread pool to avoid blocking Jarvis.
    """
    manager = get_skills_manager()
    loop = asyncio.get_event_loop()
    
    def execute():
        return manager.handle_skill_call(skill_name, command, args)
    
    result = await loop.run_in_executor(None, execute)
    return result


if __name__ == "__main__":
    # Test the skills manager
    manager = get_skills_manager()
    
    print("\n" + "="*60)
    print("OpenClaw Skills Manager - Test Mode")
    print("="*60)
    
    print(manager.list_skills())
    
    print("\n" + "="*60)
    print("Sample skill details (gemini):")
    print("="*60)
    print(manager.get_skill_help("gemini"))
    
    print("\n✅ Skills Manager ready for Jarvis integration!")
