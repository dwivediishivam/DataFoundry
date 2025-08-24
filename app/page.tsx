'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { AnalysisResults } from '@/components/AnalysisResults'
import { Loader2, TrendingUp } from 'lucide-react'

export default function Home() {
  const [idea, setIdea] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)

  const handleAnalyze = async () => {
    if (!idea.trim()) return
    
    setLoading(true)
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idea }),
      })
      
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Analysis failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <TrendingUp className="h-8 w-8 text-blue-600 mr-2" />
            <h1 className="text-4xl font-bold text-gray-900">DataFoundry</h1>
          </div>
          <p className="text-xl text-gray-600">AI-Powered Startup Idea Analysis</p>
          <p className="text-sm text-gray-500 mt-2">Get data-driven insights to validate your business ideas</p>
        </div>

        <div className="max-w-4xl mx-auto">
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Describe Your Startup Idea</CardTitle>
              <CardDescription>
                Provide a detailed description of your business idea. The more specific you are, the better insights we can provide.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                value={idea}
                onChange={(e) => setIdea(e.target.value)}
                placeholder="Example: An on-demand courier service using drones and small aircraft for same-day delivery in urban areas. The platform would connect businesses needing urgent deliveries with certified pilots operating lightweight aircraft..."
                className="min-h-[120px] resize-none"
              />
              <div className="mt-4">
                <Button 
                  onClick={handleAnalyze} 
                  disabled={loading || !idea.trim()}
                  className="w-full sm:w-auto"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    'Analyze Idea'
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {results && <AnalysisResults data={results} />}
        </div>
      </div>
    </div>
  )
}