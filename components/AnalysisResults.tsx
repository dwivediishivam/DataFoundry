'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts'
import { TrendingUp, TrendingDown, AlertTriangle, CheckCircle, DollarSign, Users, Target } from 'lucide-react'

interface AnalysisData {
  market_analysis: {
    tam: number
    sam: number
    som: number
    growth_rate: number
    market_trends: string[]
  }
  competition: {
    direct_competitors: Array<{
      name: string
      funding: number
      market_share: number
    }>
    competitive_advantage: string
    threat_level: string
  }
  financial_projections: {
    revenue_potential: number
    break_even_timeline: number
    funding_required: number
    roi_projection: number
  }
  risks: Array<{
    category: string
    level: string
    description: string
  }>
  recommendation: {
    score: number
    verdict: string
    key_insights: string[]
  }
}

export function AnalysisResults({ data }: { data: AnalysisData }) {
  const marketData = [
    { name: 'TAM', value: data.market_analysis.tam, color: '#8884d8' },
    { name: 'SAM', value: data.market_analysis.sam, color: '#82ca9d' },
    { name: 'SOM', value: data.market_analysis.som, color: '#ffc658' },
  ]

  const competitorData = data.competition.direct_competitors.map(comp => ({
    name: comp.name,
    funding: comp.funding,
    market_share: comp.market_share
  }))

  const getScoreColor = (score: number) => {
    if (score >= 70) return 'text-green-600'
    if (score >= 50) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreIcon = (score: number) => {
    if (score >= 70) return <CheckCircle className="h-5 w-5 text-green-600" />
    if (score >= 50) return <AlertTriangle className="h-5 w-5 text-yellow-600" />
    return <TrendingDown className="h-5 w-5 text-red-600" />
  }

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            {getScoreIcon(data.recommendation.score)}
            <span className="ml-2">Overall Viability Score</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div className={`text-4xl font-bold ${getScoreColor(data.recommendation.score)}`}>
              {data.recommendation.score}/100
            </div>
            <div className="text-right">
              <p className="text-lg font-semibold">{data.recommendation.verdict}</p>
              <p className="text-sm text-gray-600">Recommendation</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Market Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Target className="h-5 w-5 mr-2" />
            Market Analysis
          </CardTitle>
          <CardDescription>Total Addressable Market (TAM), Serviceable Available Market (SAM), and Serviceable Obtainable Market (SOM)</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={marketData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip formatter={(value) => [`$${value}B`, 'Market Size']} />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <span className="font-medium">Growth Rate</span>
                <span className="text-blue-600 font-bold flex items-center">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  {data.market_analysis.growth_rate}%
                </span>
              </div>
              <div>
                <h4 className="font-medium mb-2">Key Market Trends</h4>
                <ul className="space-y-1">
                  {data.market_analysis.market_trends.map((trend, index) => (
                    <li key={index} className="text-sm text-gray-600 flex items-start">
                      <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                      {trend}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Competition Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Users className="h-5 w-5 mr-2" />
            Competitive Landscape
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium mb-4">Direct Competitors</h4>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={competitorData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip formatter={(value, name) => [
                    name === 'funding' ? `$${value}M` : `${value}%`,
                    name === 'funding' ? 'Funding' : 'Market Share'
                  ]} />
                  <Bar dataKey="funding" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="space-y-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium mb-2">Competitive Advantage</h4>
                <p className="text-sm text-gray-600">{data.competition.competitive_advantage}</p>
              </div>
              <div className="p-4 bg-yellow-50 rounded-lg">
                <h4 className="font-medium mb-2">Threat Level</h4>
                <p className="text-sm font-semibold text-yellow-700">{data.competition.threat_level}</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Financial Projections */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <DollarSign className="h-5 w-5 mr-2" />
            Financial Projections
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <p className="text-2xl font-bold text-green-600">${data.financial_projections.revenue_potential}M</p>
              <p className="text-sm text-gray-600">Revenue Potential</p>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <p className="text-2xl font-bold text-blue-600">{data.financial_projections.break_even_timeline}</p>
              <p className="text-sm text-gray-600">Months to Break Even</p>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <p className="text-2xl font-bold text-purple-600">${data.financial_projections.funding_required}M</p>
              <p className="text-sm text-gray-600">Funding Required</p>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <p className="text-2xl font-bold text-orange-600">{data.financial_projections.roi_projection}%</p>
              <p className="text-sm text-gray-600">ROI Projection</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Risk Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <AlertTriangle className="h-5 w-5 mr-2" />
            Risk Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {data.risks.map((risk, index) => (
              <div key={index} className={`p-4 rounded-lg border-l-4 ${
                risk.level === 'High' ? 'bg-red-50 border-red-500' :
                risk.level === 'Medium' ? 'bg-yellow-50 border-yellow-500' :
                'bg-green-50 border-green-500'
              }`}>
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-medium">{risk.category}</h4>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    risk.level === 'High' ? 'bg-red-100 text-red-800' :
                    risk.level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {risk.level}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{risk.description}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Key Insights */}
      <Card>
        <CardHeader>
          <CardTitle>Key Insights & Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            {data.recommendation.key_insights.map((insight, index) => (
              <li key={index} className="flex items-start">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                <span className="text-sm">{insight}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}