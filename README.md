# DataFoundry - AI-Powered Startup Analysis

DataFoundry is an intelligent platform that provides data-driven insights and analysis for startup ideas. Using AI agents and real-world data sources, it evaluates market potential, competitive landscape, financial projections, and risks to help entrepreneurs make informed decisions.

## Features

- **AI-Powered Analysis**: Uses Google Gemini to break down and analyze startup ideas
- **Market Intelligence**: Provides TAM/SAM/SOM analysis with growth projections
- **Competitive Analysis**: Identifies competitors and market positioning
- **Financial Projections**: Estimates revenue potential, funding requirements, and ROI
- **Risk Assessment**: Evaluates potential risks across multiple categories
- **Interactive Dashboard**: Beautiful charts and visualizations using Recharts
- **Real-time Insights**: 70% data-driven metrics, 30% strategic insights

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Modern UI components
- **Recharts** - Data visualization library
- **Lucide React** - Icon library

### Backend
- **FastAPI** - High-performance Python web framework
- **Google Gemini** - LLM for intelligent analysis and idea breakdown
- **Portia AI** - Multi-agent orchestration and workflow management
- **SerpAPI** - Real-time search data for market research
- **HTTPX** - Async HTTP client for API integration
- **Asyncio** - Concurrent execution of analysis agents
- **Pydantic** - Data validation and serialization

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Google Gemini API key
- Portia AI API key (for enhanced agent orchestration)
- SerpAPI key (for real-time market data)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd datafoundry
```

### 2. Backend Setup

```bash
# Make scripts executable
chmod +x start-backend.sh start-frontend.sh

# Start backend (will create virtual environment and install dependencies)
./start-backend.sh
```

On first run, you'll need to add your API keys to `backend/.env`:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here
PORTIA_API_KEY=your_portia_ai_api_key_here
SERPAPI_KEY=your_serpapi_key_here
WORLD_BANK_API_KEY=your_world_bank_api_key_here
```

### 3. Frontend Setup

In a new terminal:

```bash
# Start frontend (will install dependencies)
./start-frontend.sh
```

### 4. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Usage

1. **Enter Your Startup Idea**: Provide a detailed description of your business concept
2. **Get Analysis**: The system will analyze your idea across multiple dimensions
3. **Review Results**: Examine market data, competition, financials, and risks
4. **Make Decisions**: Use the overall viability score and insights to guide your strategy

### Example Input

```
An on-demand courier service using drones and small aircraft for same-day delivery in urban areas. The platform would connect businesses needing urgent deliveries with certified pilots operating lightweight aircraft. Target customers include medical facilities, legal firms, and e-commerce businesses requiring rapid document or small package delivery within 50-mile radius of major cities.
```

## Architecture

### Agent System

DataFoundry uses a sophisticated multi-agent architecture with **Portia AI** orchestration:

#### Portia AI Integration

**Portia AI** serves as the central orchestration platform that coordinates specialized agents for comprehensive startup analysis. The system leverages Portia's workflow management capabilities to execute complex, multi-step analysis processes.

**Key Portia AI Features Used:**
- **Agent Orchestration**: Coordinates multiple specialized agents in parallel and sequential workflows
- **Task Management**: Manages complex analysis tasks with dependencies and context sharing
- **Workflow Execution**: Handles timeout management, error recovery, and result aggregation
- **Tool Integration**: Provides agents with specialized tools for market research, competitive analysis, and data gathering

#### Specialized Agents

1. **Market Research Agent** (`market_researcher`)
   - **Role**: Market Research Analyst with 10+ years experience
   - **Tools**: `market_data_api`, `trend_analysis`, `industry_reports`
   - **Function**: Analyzes TAM/SAM/SOM, market trends, and growth opportunities using real-time data

2. **Competitive Intelligence Agent** (`competitor_analyst`)
   - **Role**: Competitive Intelligence Specialist
   - **Tools**: `competitor_database`, `funding_tracker`, `market_share_analysis`
   - **Function**: Identifies competitors, analyzes funding data, and assesses competitive threats

3. **Financial Modeling Agent** (`financial_analyst`)
   - **Role**: Senior Financial Analyst and Investment Expert
   - **Tools**: `financial_modeling`, `valuation_tools`, `benchmark_data`
   - **Function**: Creates realistic financial projections based on industry benchmarks

4. **Risk Assessment Agent** (`risk_assessor`)
   - **Role**: Risk Management Consultant
   - **Tools**: `risk_database`, `regulatory_tracker`, `industry_risk_models`
   - **Function**: Identifies market, operational, regulatory, and financial risks

5. **Strategic Advisory Agent** (`strategic_advisor`)
   - **Role**: Senior Strategic Business Consultant
   - **Tools**: `synthesis_framework`, `decision_models`, `strategic_templates`
   - **Function**: Synthesizes all analyses into actionable strategic recommendations

#### Workflow Architecture

```
Portia AI Orchestrator
├── LLM Breakdown (Gemini) → Idea Categorization
├── Parallel Agent Execution
│   ├── Market Research Agent → Real-time market data
│   ├── Competitor Agent → SerpAPI + curated databases
│   ├── Financial Agent → Industry benchmarks + projections
│   └── Risk Agent → Multi-source risk analysis
└── Strategic Synthesis → Final recommendations
```

#### Fallback System

The system includes intelligent fallbacks:
- **Primary**: Portia AI orchestrated workflow with specialized tools
- **Secondary**: Direct agent execution with API integrations
- **Tertiary**: Curated data with intelligent algorithms

Each agent uses Portia AI's specialized tools for data gathering and analysis, working together in a coordinated workflow managed by the Portia orchestrator.

### Data Flow

```
User Input 
    ↓
LLM Breakdown (Gemini)
    ↓
Portia AI Orchestrator
    ├── Market Research Agent (SerpAPI + Industry Data)
    ├── Competitor Agent (SerpAPI + Curated Databases)  
    ├── Financial Agent (Industry Benchmarks)
    └── Risk Agent (Multi-source Analysis)
    ↓
Data Aggregation & Synthesis
    ↓
Strategic Recommendations (Portia AI)
    ↓
Dashboard Visualization (Next.js + Recharts)
```

#### API Integration Details

- **Portia AI API**: `https://api.portia.dev/v1` - Workflow orchestration and agent management
- **Google Gemini**: Idea breakdown and natural language processing
- **SerpAPI**: Real-time search data for market research and competitor analysis
- **Fallback Systems**: Curated databases and algorithmic analysis when APIs are unavailable

## API Endpoints

### POST /analyze
Analyzes a startup idea and returns comprehensive insights.

**Request:**
```json
{
  "idea": "Your detailed startup idea description"
}
```

**Response:**
```json
{
  "market_analysis": {
    "tam": 1200,
    "sam": 120,
    "som": 12,
    "growth_rate": 8.5,
    "market_trends": ["trend1", "trend2"]
  },
  "competition": {
    "direct_competitors": [...],
    "competitive_advantage": "...",
    "threat_level": "Medium"
  },
  "financial_projections": {
    "revenue_potential": 150,
    "break_even_timeline": 18,
    "funding_required": 25,
    "roi_projection": 35
  },
  "risks": [...],
  "recommendation": {
    "score": 75,
    "verdict": "Recommended",
    "key_insights": [...]
  }
}
```

## Portia AI Configuration

### Setting Up Portia AI

1. **Get API Key**: Sign up at [Portia AI](https://portia.dev) and obtain your API key
2. **Add to Environment**: Set `PORTIA_API_KEY` in your `backend/.env` file
3. **Agent Configuration**: Agents are pre-configured with specialized roles and tools

### Portia AI Workflow Structure

The system uses Portia AI's workflow execution API with the following structure:

```python
{
    "agents": [
        {
            "name": "market_researcher",
            "role": "Market Research Analyst", 
            "goal": "Analyze market opportunity and trends",
            "backstory": "Expert with 10+ years in market analysis...",
            "tools": ["market_data_api", "trend_analysis"]
        }
        # ... other agents
    ],
    "tasks": [
        {
            "description": "Analyze market size and growth for startup idea",
            "agent": "market_researcher",
            "expected_output": "Structured market analysis with TAM/SAM/SOM"
        }
        # ... other tasks
    ],
    "process": "sequential",
    "timeout": 300
}
```

### Monitoring Portia AI Execution

- **Logs**: Check backend logs for Portia AI workflow status
- **Fallback**: System automatically falls back to direct agents if Portia AI is unavailable
- **Timeout**: 5-minute timeout for complex analyses

## Development

### Adding New Agents

#### For Portia AI Integration:
1. Define agent in `PortiaOrchestrator._create_agents()`:
   ```python
   PortiaAgent(
       name="new_agent",
       role="Agent Role",
       goal="Agent objective", 
       backstory="Agent expertise",
       tools=["tool1", "tool2"]
   )
   ```

2. Add corresponding task in `_create_analysis_workflow()`:
   ```python
   PortiaTask(
       description="Task description",
       agent="new_agent",
       expected_output="Expected result format"
   )
   ```

#### For Direct Agent Implementation:
1. Create agent class in `backend/agents/`
2. Implement the `analyze()` method
3. Add to orchestrator fallback system
4. Update data aggregation logic

### Extending Data Sources

- Add new API integrations in respective agent files
- Implement error handling and fallback data
- Update the data normalization logic

### Frontend Customization

- Modify components in `components/`
- Update charts and visualizations in `AnalysisResults.tsx`
- Customize styling with Tailwind classes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For questions or issues, please open a GitHub issue or contact the development team.