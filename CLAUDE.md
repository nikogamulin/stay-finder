# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main accommodation search agent
python3 accommodation_search_agent/agent.py
```

## Environment Setup

This project requires a Google AI Studio API key:
1. Create a `.env` file in the project root
2. Add: `GOOGLE_API_KEY=your_gemini_api_key_here`
3. Set `GEMINI_MODEL` environment variable for the master orchestrator model

## Architecture Overview

This is a hierarchical multi-agent system built with Google ADK for vacation accommodation search. The system follows a 4-phase orchestrated workflow:

### Agent Hierarchy

**Root Agent**: `accommodation_manager_agent` - Master orchestrator that manages the entire planning process through 4 sequential phases

**Phase 1-3 Tools** (used as AgentTools):
- `request_parser_agent` - Extracts destination, dates, number of people, and preferences
- `location_refinement_agent` - Refines general destinations into specific locations
- `search_string_generator_agent` - Creates structured search query sets

**Phase 4 Sub-Agent**: `accomodation_sequential_agent` - Handles accommodation search and result presentation
- Uses `LoopAgent` for iterative search term processing (max 10 iterations)
- Contains nested sub-agents for search term selection, browsing, and result processing
- Includes `results_presenter_agent` for final output formatting

### Key Patterns

1. **Agent vs Tool Usage**: Phases 1-3 use agents as tools (AgentTool wrapper), Phase 4 uses sub-agents
2. **Sequential Processing**: The main workflow is strictly sequential through the 4 phases
3. **Loop Processing**: The accommodation browser uses a LoopAgent for iterative search processing
4. **Shared Callbacks**: All agents use common callbacks from `shared_lib/callbacks.py`

### Model Configuration

- Main orchestrator uses `os.getenv("GEMINI_MODEL")`
- Sub-agents typically use `gemini-2.5-flash-preview-05-20`
- All agents include `output_key` parameter for structured data flow

### Critical Requirements

The system requires successful completion of core information extraction (destination, dates, number of people) in Phase 1 before proceeding to subsequent phases.