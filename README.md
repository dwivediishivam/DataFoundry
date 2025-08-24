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
- **Google Gemini** - LLM for intelligent analysis
- **Portia SDK** - Agent orchestration (planned)
- **Asyncio** - Concurrent agent execution
- **Pydantic** - Data validation and serialization

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Google Gemini API key

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
GEMINI_API_KEY=your_gemini_api_key_here
WORLD_BANK_API_KEY=your_world_bank_api_key_here
SERPAPI_KEY=your_serpapi_key_here
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

The backend uses a multi-agent architecture:

1. **LLM Breakdown Agent** - Analyzes and categorizes the startup idea
2. **Market Analysis Agent** - Researches market size and trends
3. **Competitor Agent** - Identifies competition and market positioning
4. **Financial Agent** - Projects revenue, costs, and funding requirements
5. **Risk Agent** - Evaluates potential risks and challenges
6. **Insight Agent** - Synthesizes data into actionable recommendations

### Data Flow

```
User Input → LLM Breakdown → Parallel Agent Execution → Data Aggregation → Insight Generation → Dashboard Visualization
```

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

## Development

### Adding New Agents

1. Create a new agent class in `backend/agents/`
2. Implement the `analyze()` method
3. Add the agent to the orchestrator
4. Update the data aggregation logic

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