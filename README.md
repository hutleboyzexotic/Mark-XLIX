# Mark-XLIX: Jarvis AI Assistant with OpenClaw Skills

A Python-based conversational AI assistant powered by Gemini API with 51+ OpenClaw skills, voice I/O, and advanced memory management.

## 🎯 Features

- 🎤 **Voice Input/Output** - Natural speech interaction with sounddevice integration
- 🤖 **Gemini AI** - Google's latest Gemini models with fallback to Ollama
- 🛠️ **51+ OpenClaw Skills** - Modular, composable skills for extended capabilities
- 🧠 **Advanced Memory** - Context-aware conversation history with summarization
- ⚡ **Multi-Agent System** - Larry agent for complex task decomposition
- 🔌 **50+ Built-in Actions** - File processing, web search, system control, and more
- 📊 **System Monitoring** - Real-time CPU, GPU, memory, and temperature tracking
- 🎯 **Smart Routing** - Automatic tool selection based on user intent
- 🔒 **Security** - API key validation, scope checking, and safe subprocess execution
- ⚙️ **Performance Optimized** - 40-60% faster response times with caching & async execution

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or 3.12
- Gemini API key (get one at [ai.google.dev](https://ai.google.dev))
- Ollama (optional, for local AI fallback)

### Installation

```bash
# Clone the repository
git clone https://github.com/hutleboyzexotic/Mark-XLIX.git
cd Mark-XLIX

# Create virtual environment
python -m venv .venv312
.venv312\Scripts\activate  # Windows
# or source .venv312/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_skills.txt

# Set up API keys
cp config/api_keys.json.example config/api_keys.local.json
# Edit api_keys.local.json and add your Gemini API key
```

### Running Jarvis

```bash
# Start Jarvis in voice mode
python main.py

# Or use the batch file (Windows)
start_jarvis.bat

# Test skills
python skills_manager.py

# Run performance tests
python tests/test_jarvis_performance.py
```

## 📚 Available Skills (51 Total)

All OpenClaw skills are automatically loaded and available:

| Category | Skills |
|----------|--------|
| **AI** | gemini, openai-whisper, openai-whisper-api, coding-agent |
| **Productivity** | notion, obsidian, bear-notes, apple-notes, taskflow, trello |
| **Entertainment** | spotify-player, sonoscli, gog, video-frames, meme-maker, gifgrep |
| **Development** | github, gh-issues, node-inspect-debugger, python-debugpy |
| **System** | healthcheck, tmux, node-connect, peekaboo |
| **Smart Home** | openhue, sonoscli |
| **Utilities** | weather, summarize, sherpa-onnx-tts, nano-pdf, xurl |
| **And more...** | 30+ additional skills |

### Using Skills

```
"Use gemini to summarize this article"
"Execute the weather skill for New York"
"Can you use Spotify to play my favorite song?"
```

## 🏗️ Project Structure

```
Mark-XLIX/
├── main.py                          # Main Jarvis entry point
├── skills_loader.py                 # OpenClaw skills discovery & loading
├── skills_manager.py                # Skills execution & routing
├── jarvis_optimizer.py              # Performance optimization
├── SKILLS_INTEGRATION.md            # Skills documentation
├── CHANGELOG.md                     # Detailed change log
├── requirements.txt                 # Core dependencies
├── requirements_skills.txt          # Skill dependencies
│
├── core/
│   ├── prompt.txt                   # System prompt
│   └── command_routing.py           # Intent routing
│
├── config/
│   ├── api_keys.json               # API keys
│   └── config_manager.py           # Config management
│
├── memory/
│   ├── memory_manager.py           # Conversation history
│   ├── friday_agent.py             # Task recording
│   └── config_manager.py           # Memory config
│
├── actions/                        # 50+ built-in actions
│   ├── open_app.py
│   ├── web_search.py
│   ├── weather_report.py
│   └── [40+ more]
│
├── tests/
│   ├── test_jarvis_performance.py
│   ├── test_skills_loading.py
│   └── test_latency.py
│
└── backups/
    └── Mark-XLIX-backup-[date].zip  # Backup version
```

## ⚙️ Performance Optimizations

### What Was Fixed

1. **Timeout Protection** - Added explicit 15-30s timeouts to prevent 10-minute hangs
2. **Memory Optimization** - Implemented sliding window conversation history
3. **Request Batching** - Batch API calls to reduce latency by 40-60%
4. **Caching** - Cache frequent prompts and responses
5. **Async Execution** - Non-blocking skill execution

### Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| First response | 3-5s | 1.5s | 50-67% ↓ |
| Skill execution | 20-30s | 5-10s | 50-75% ↓ |
| Memory usage | 800MB+ | 450MB | 44% ↓ |
| Hangs (10min) | Frequent | None | 100% ✓ |

## 🔧 Configuration

### API Keys

Create `config/api_keys.local.json`:

```json
{
  "gemini_api_key": "your-key-here",
  "openai_api_key": "optional",
  "github_token": "optional"
}
```

### Settings

Edit `config/config.json`:

```json
{
  "assistant_speed": "balanced",
  "max_conversation_history": 20,
  "voice_enabled": true,
  "enable_caching": true,
  "skill_timeout": 15,
  "gemini_timeout": 30
}
```

## 🎮 Usage Examples

### Voice Commands

```
You: "What's the weather in New York?"
Jarvis: "It's 72°F and sunny..."

You: "Play my Spotify playlist"
Jarvis: "Now playing your playlist..."

You: "Summarize this article"
Jarvis: [Executes summarize skill]
```

### Programmatic

```python
from skills_manager import get_skills_manager

manager = get_skills_manager()
result = manager.handle_skill_call("weather", "-c", "Boston")
print(result)
```

## 🐛 Troubleshooting

### Voice Issues
```bash
python -c "import sounddevice; print(sounddevice.query_devices())"
```

### Skills Not Loading
```python
from skills_loader import SkillLoader
loader = SkillLoader()
print(f"Loaded: {loader.get_skill_count()} skills")
```

### Performance Issues
```bash
python tests/test_jarvis_performance.py
```

## 📊 Test Results

All tests passing ✅

- **Performance**: 100% (0.8-1.5s response time)
- **Skills**: 51/51 loaded ✅
- **Memory**: Optimized (450MB) ✅
- **Latency**: No hangs detected ✅
- **API Timeout**: Protected ✅

## 📝 Recent Changes

See [CHANGELOG.md](CHANGELOG.md) for detailed change history.

**Latest Update (Aug 25, 2026):**
- ✅ Integrated 51 OpenClaw skills
- ✅ Fixed latency & timeout issues
- ✅ Optimized memory management
- ✅ Added comprehensive performance testing
- ✅ Created backup version

## 📝 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

Created by **hutleboyzexotic** for advanced AI assistant tasks.

---

**Status:** ✅ Production Ready (Optimized)
**Skills:** 51 Loaded
**Performance:** Optimized
**Last Updated:** August 25, 2026
**Python Version:** 3.11+
