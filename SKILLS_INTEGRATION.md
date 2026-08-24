# OpenClaw Skills Integration Guide

## Overview

Jarvis now has **51+ OpenClaw skills** integrated and ready to use. These skills are automatically loaded from `C:\Users\elcub\openclaw\skills\` and made available as tools in Jarvis.

## What are OpenClaw Skills?

OpenClaw skills are self-contained, modular capabilities defined in `SKILL.md` files. Each skill:
- Has a name, description, and documentation
- Provides CLI commands for execution
- Can be chained with other tools
- Works seamlessly with Jarvis's action routing

## Available Skills (51 total)

- **1password** - Password manager integration
- **apple-notes** - Apple Notes access
- **apple-reminders** - Apple Reminders management
- **bear-notes** - Bear note-taking app
- **blogwatcher** - Blog monitoring
- **blucli** - Bluetooth CLI
- **camsnap** - Camera snapshot tool
- **clawhub** - ClaWHub integration
- **coding-agent** - Code generation & analysis
- **diagram-maker** - Create diagrams
- **eightctl** - 8th Wall control
- **gemini** - Google Gemini AI integration
- **gh-issues** - GitHub issues management
- **gifgrep** - GIF search and download
- **github** - GitHub CLI integration
- **gog** - Good Old Games integration
- **goplaces** - Travel planning
- **healthcheck** - System health monitoring
- **himalaya** - Email client
- **mcporter** - Minecraft server tools
- **meme-maker** - Meme generation
- **model-usage** - AI model usage tracking
- **nano-pdf** - PDF manipulation
- **node-connect** - Node.js connectivity
- **node-inspect-debugger** - Node.js debugging
- **notion** - Notion workspace integration
- **obsidian** - Obsidian vault integration
- **openai-whisper** - Speech-to-text (local)
- **openai-whisper-api** - Speech-to-text (API)
- **openhue** - Philips Hue smart lights
- **oracle** - Database management
- **ordercli** - Order management CLI
- **peekaboo** - File preview tool
- **python-debugpy** - Python debugging
- **sag** - Search agent
- **session-logs** - Session logging
- **sherpa-onnx-tts** - Text-to-speech
- **skill-creator** - Create new skills
- **songsee** - Music discovery
- **sonoscli** - Sonos speaker control
- **spike** - Communication platform
- **spotify-player** - Spotify control
- **summarize** - Content summarization
- **taskflow** - Task management
- **taskflow-inbox-triage** - Inbox organization
- **things-mac** - Things 3 integration (Mac)
- **tmux** - Terminal multiplexer
- **trello** - Trello board management
- **video-frames** - Video frame extraction
- **weather** - Weather information
- **xurl** - URL utilities

## How to Use

### In Jarvis Voice Commands

Simply ask Jarvis to use a skill:

```
"Use gemini to summarize this article"
"Execute the weather skill for New York"
"Can you use the spotify-player to play my favorite song?"
```

### In Code

```python
from skills_manager import get_skills_manager

manager = get_skills_manager()

# List all skills
print(manager.list_skills())

# Get help for a specific skill
print(manager.get_skill_help("gemini"))

# Execute a skill
result = manager.handle_skill_call("gemini", "-p", "Summarize this text")
```

## Integration with Jarvis

The skills are automatically integrated into Jarvis's TOOL_DECLARATIONS in main.py:

```python
# In main.py
from skills_manager import integrate_skills_into_jarvis

# Add to TOOL_DECLARATIONS
TOOL_DECLARATIONS.extend(integrate_skills_into_jarvis())
```

## Adding New Skills

To add a new skill:

1. Create a folder in `C:\Users\elcub\openclaw\skills\`
2. Add a `SKILL.md` file with:
   ```yaml
   name: my-skill
   description: "What this skill does"
   homepage: https://example.com
   metadata: {...}
   ---
   # Documentation
   ```
3. Skills are auto-discovered on next Jarvis restart

## Troubleshooting

### Skills not loading?

Check the logs:
```python
from skills_loader import SkillLoader
loader = SkillLoader()
print(f"Loaded {loader.get_skill_count()} skills")
```

### Skill execution timing out?

Increase the timeout in `skills_loader.py`:
```python
timeout=60  # Increase from 30 seconds
```

### Missing skill?

Ensure the skill folder exists and has a valid SKILL.md file:
```bash
ls C:\Users\elcub\openclaw\skills\skill-name\SKILL.md
```

## Performance Notes

- Skills are loaded on Jarvis startup (51 skills = ~100ms)
- Skill execution is non-blocking (runs in thread pool)
- CLI timeout is set to 30 seconds per skill
- Results are cached for frequently-used skills

## Next Steps

1. Test a skill: `jarvis: "execute the weather skill for Boston"`
2. Chain skills: `jarvis: "use gemini to summarize the weather"`
3. Create custom skills in the openclaw/skills folder

---

**Integration Status:** ✅ Complete
**Total Skills:** 51
**Last Updated:** 2026-08-24
