# ADK Accommodation Search Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285f4.svg)](https://google.github.io/adk-docs/)

A hierarchical multi-agent system built with Google's Agent Development Kit (ADK) for intelligent vacation accommodation search. The system uses web browsing capabilities via MCP (Model Context Protocol) to search and analyze accommodation options across multiple platforms.

## Architecture Overview

This project implements a sophisticated 4-phase orchestrated workflow:

### Agent Hierarchy

**Root Agent**: `accommodation_manager_agent` - Master orchestrator that manages the entire planning process

**Phase 1-3 Tools** (used as AgentTools):
- `request_parser_agent` - Extracts destination, dates, number of people, and preferences
- `location_refinement_agent` - Refines general destinations into specific locations  
- `search_string_generator_agent` - Creates structured search query sets

**Phase 4 Sub-Agent**: `accomodation_sequential_agent` - Handles accommodation search and result presentation
- Uses `LoopAgent` for iterative search term processing (max 10 iterations)
- Contains nested sub-agents for search term selection, browsing, and result processing
- Includes `results_presenter_agent` for final output formatting

### Key Features

- **Web Browsing**: Automated web search and data extraction using BrowserMCP
- **Multi-Platform Search**: Searches across multiple accommodation platforms
- **Intelligent Parsing**: Extracts structured data from natural language requests
- **Iterative Refinement**: Progressively refines search results through multiple iterations
- **Comprehensive Results**: Presents formatted accommodation options with details

## Project Structure

```
adk-accommodation-search_agent/
├── accommodation_search_agent/          # Main multi-agent system
│   ├── agent.py                        # Master orchestrator
│   ├── prompt.py                       # System prompts
│   ├── shared_lib/
│   │   └── callbacks.py               # Shared callback functions
│   └── sub_agents/
│       ├── request_parser_agent/       # Phase 1: Parse user requests
│       ├── location_refinement_agent/  # Phase 2: Refine locations
│       ├── search_string_generator_agent/ # Phase 3: Generate search terms
│       ├── accommodation_browser_agent/ # Phase 4: Browser orchestrator
│       └── results_presenter_agent/    # Final results formatting
├── accomodation_search_single_agent/   # Simplified test agent
│   └── agent.py                       # Single browser agent for testing
├── requirements.txt                    # Python dependencies
├── .env                               # Environment configuration
└── README.md                          # This file
```

## Prerequisites

- Python 3.8 or newer
- Node.js 16+ (for BrowserMCP)
- Google AI Studio API key
- Internet connection for web browsing

## Installation

### 1. Clone and Set Up Environment

```bash
# Clone the repository
git clone <repository-url>
cd adk-accommodation-search_agent

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Node.js and BrowserMCP

#### Install Node.js
Visit [nodejs.org](https://nodejs.org/) and install the LTS version, or use a package manager:

```bash
# On macOS with Homebrew
brew install node

# On Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
npx --version
```

#### Install BrowserMCP
The project uses [BrowserMCP](https://browsermcp.io) for web browsing capabilities:

```bash
# Install BrowserMCP globally (recommended)
npm install -g @browsermcp/mcp

# Or install the latest version on-demand (used by the agents)
npx @browsermcp/mcp@latest --help
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Google AI Studio API Key (required)
GOOGLE_API_KEY=your_gemini_api_key_here

# Master orchestrator model (optional, defaults to gemini-2.0-flash)
GEMINI_MODEL=gemini-2.0-flash
```

To get your Google AI Studio API key:
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Go to [API Keys section](https://aistudio.google.com/app/apikeys)
3. Create a new API key
4. Copy the key to your `.env` file

## Usage

### Running the Full System

Use the ADK CLI to run the complete accommodation search system:

```bash
# Start the main orchestrator agent
adk run accommodation_search_agent
```

### Running the Test Agent

For testing and development, use the simplified single agent:

```bash
# Start the single browser agent
adk run accomodation_search_single_agent
```

### Example Queries

Here are some example accommodation search requests you can try:

#### Basic Apartment Search
```
I am looking for an apartment for 3 persons in Barcelona, Spain from June 15th to June 22nd, 2024. Budget around 150 euros per night.
```

#### Detailed Family Vacation
```
We need family-friendly accommodation in Orlando, Florida for 2 adults and 2 children (ages 8 and 12) from December 20th to December 27th, 2023. We prefer vacation rentals with a pool and kitchen, budget up to $200 per night.
```

#### Business Trip
```
Looking for a hotel in downtown Tokyo, Japan for 1 person from March 10-15, 2024. Need good WiFi for work, near public transportation, budget flexible up to $300/night.
```

#### Romantic Getaway
```
Planning a romantic weekend in Santorini, Greece for 2 people from September 5-8, 2024. Looking for boutique hotels or villas with sea views, budget around 400 euros per night.
```

#### Group Travel
```
Need accommodation for 8 people (4 couples) in Prague, Czech Republic from August 1-7, 2024. Prefer apartment rentals or guesthouses that can accommodate the group together, budget 100-150 euros per night total.
```

#### Specific Requirements
```
Looking for pet-friendly accommodation in Portland, Oregon for 2 adults and 1 dog from July 10-14, 2024. Prefer places with outdoor space or nearby parks, budget up to $180 per night.
```

### Expected Workflow

When you submit a request, the system will:

1. **Parse Request** - Extract destination, dates, guest count, and preferences
2. **Refine Location** - Convert general locations to specific searchable areas
3. **Generate Search Terms** - Create optimized search queries for different platforms
4. **Browse & Search** - Automatically search accommodation websites
5. **Present Results** - Format and present accommodation options with details

## Technical Details

### Timeout Configuration

The system includes comprehensive timeout handling to prevent the common "5-second timeout" errors in MCP connections:

- **ClientSession Timeout**: Increased from 5 to 60 seconds
- **Browser Timeouts**: Extended navigation and operation timeouts
- **Playwright Settings**: Configured for reliable web browsing

### Model Configuration

- **Main Orchestrator**: Uses `GEMINI_MODEL` environment variable (default: gemini-2.0-flash)
- **Sub-agents**: Typically use `gemini-2.5-flash-preview-05-20` for efficiency
- **Output Handling**: All agents include `output_key` parameters for structured data flow

### Error Handling

The system includes robust error handling for:
- Network timeouts and connection issues
- Web page loading failures
- Invalid search parameters
- API rate limiting

## Troubleshooting

### Common Issues

**"Timed out while waiting for response" Error**
- This has been resolved with timeout patches in the codebase
- Ensure you're using the latest version of the agents

**BrowserMCP Installation Issues**
```bash
# Clear npm cache and reinstall
npm cache clean --force
npm install -g @browsermcp/mcp@latest
```

**API Key Issues**
- Verify your `.env` file is in the project root
- Check that your Google AI Studio API key is valid
- Ensure the key has appropriate permissions

**Node.js Version Issues**
```bash
# Check Node.js version (should be 16+)
node --version

# Update Node.js if needed
npm install -g n
n latest
```

### Debugging

**Enable Verbose Logging**
```bash
# Set debug environment variable
export DEBUG=*
adk run accommodation_search_agent
```

**Check Agent Logs**
```bash
# ADK logs are typically in /tmp/agents_log/
tail -f /tmp/agents_log/agent.latest.log
```

**Test BrowserMCP Directly**
```bash
# Test BrowserMCP installation
npx @browsermcp/mcp@latest --help
```

## Development

### Adding New Search Platforms

To add support for new accommodation platforms:

1. Update search term generation in `search_string_generator_agent`
2. Modify browsing logic in `search_term_browser_agent`
3. Update result extraction patterns in `browsing_results_agent`

### Customizing Search Logic

The search behavior can be customized by:
- Modifying prompts in the respective `prompt.py` files
- Adjusting iteration limits in the `LoopAgent` configuration
- Updating callback functions in `shared_lib/callbacks.py`

### Testing Changes

Use the single agent for rapid testing:
```bash
# Test specific functionality
adk run accomodation_search_single_agent
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both single and full agent systems
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ **Free to use** for any purpose (personal, commercial, educational)
- ✅ **Free to modify** and create derivative works
- ✅ **Free to distribute** original or modified versions
- ✅ **No warranty** - use at your own risk
- ✅ **Attribution required** - keep the copyright notice

Perfect for showcasing AI development skills and encouraging community contributions!

## Support

For issues and questions:
- Check the troubleshooting section above
- Review ADK documentation: [Google ADK Docs](https://google.github.io/adk-docs/)
- BrowserMCP documentation: [browsermcp.io](https://browsermcp.io)

---

*Built with Google Agent Development Kit (ADK) and BrowserMCP*