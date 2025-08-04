import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog.jsx'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Phone, 
  Users, 
  TrendingUp, 
  Clock, 
  PhoneCall, 
  UserPlus, 
  FileText, 
  BarChart3,
  Settings,
  Play,
  Pause,
  Upload,
  Download,
  MessageSquare,
  Mail,
  Calendar,
  Target,
  Zap,
  Activity,
  DollarSign,
  CheckCircle,
  XCircle,
  AlertCircle
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'
import './App.css'

// Mock data for demonstration
const mockAnalytics = {
  total_leads: 156,
  total_calls: 89,
  conversion_rate: 23.5,
  avg_call_duration: 4.2,
  leads_by_status: {
    'new': 45,
    'contacted': 67,
    'qualified': 32,
    'converted': 12
  },
  calls_by_outcome: {
    'appointment': 21,
    'interested': 34,
    'callback': 18,
    'not_interested': 16
  },
  recent_calls: [
    { id: 1, lead_name: 'Mario Rossi', lead_company: 'Rossi Restaurant', status: 'completed', outcome: 'appointment', duration: 320, created_at: '2025-01-08T10:30:00Z' },
    { id: 2, lead_name: 'Sarah Johnson', lead_company: 'Johnson Auto', status: 'completed', outcome: 'interested', duration: 245, created_at: '2025-01-08T09:15:00Z' },
    { id: 3, lead_name: 'David Chen', lead_company: 'Chen Law Firm', status: 'in_progress', outcome: null, duration: 0, created_at: '2025-01-08T11:45:00Z' }
  ]
}

const mockLeads = [
  { id: 1, name: 'Mario Rossi', phone: '+1-555-0101', email: 'mario@rossirestaurant.com', company: 'Rossi Italian Restaurant', industry: 'restaurant', status: 'qualified', score: 85, calls_count: 2 },
  { id: 2, name: 'Sarah Johnson', phone: '+1-555-0102', email: 'sarah@johnsonauto.com', company: 'Johnson Auto Repair', industry: 'car_service', status: 'contacted', score: 65, calls_count: 1 },
  { id: 3, name: 'David Chen', phone: '+1-555-0103', email: 'david@chenlaw.com', company: 'Chen & Associates Law Firm', industry: 'ai_receptionist', status: 'new', score: 0, calls_count: 0 }
]

// Dashboard Overview Component
function Dashboard() {
  const [analytics, setAnalytics] = useState(mockAnalytics)
  const [isLoading, setIsLoading] = useState(false)

  const chartData = [
    { name: 'Mon', calls: 12, conversions: 3 },
    { name: 'Tue', calls: 19, conversions: 5 },
    { name: 'Wed', calls: 15, conversions: 4 },
    { name: 'Thu', calls: 22, conversions: 6 },
    { name: 'Fri', calls: 18, conversions: 4 },
    { name: 'Sat', calls: 8, conversions: 2 },
    { name: 'Sun', calls: 5, conversions: 1 }
  ]

  const pieData = Object.entries(analytics.leads_by_status).map(([status, count]) => ({
    name: status.charAt(0).toUpperCase() + status.slice(1),
    value: count
  }))

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">AI Voice Sales Agent Dashboard</h1>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            Export Report
          </Button>
          <Button size="sm">
            <Activity className="w-4 h-4 mr-2" />
            Live Monitor
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Leads</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.total_leads}</div>
            <p className="text-xs text-muted-foreground">+12% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Calls</CardTitle>
            <Phone className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.total_calls}</div>
            <p className="text-xs text-muted-foreground">+8% from last week</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.conversion_rate}%</div>
            <p className="text-xs text-muted-foreground">+2.1% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Call Duration</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics.avg_call_duration}m</div>
            <p className="text-xs text-muted-foreground">-0.3m from last week</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Call Activity</CardTitle>
            <CardDescription>Daily calls and conversions over the past week</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="calls" stroke="#8884d8" strokeWidth={2} />
                <Line type="monotone" dataKey="conversions" stroke="#82ca9d" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Lead Status Distribution</CardTitle>
            <CardDescription>Current status of all leads in the system</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Call Activity</CardTitle>
          <CardDescription>Latest calls made by the AI agent</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Lead</TableHead>
                <TableHead>Company</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Outcome</TableHead>
                <TableHead>Duration</TableHead>
                <TableHead>Time</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {analytics.recent_calls.map((call) => (
                <TableRow key={call.id}>
                  <TableCell className="font-medium">{call.lead_name}</TableCell>
                  <TableCell>{call.lead_company}</TableCell>
                  <TableCell>
                    <Badge variant={call.status === 'completed' ? 'default' : 'secondary'}>
                      {call.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    {call.outcome ? (
                      <Badge variant={call.outcome === 'appointment' ? 'default' : 'outline'}>
                        {call.outcome}
                      </Badge>
                    ) : (
                      <span className="text-muted-foreground">-</span>
                    )}
                  </TableCell>
                  <TableCell>{call.duration > 0 ? `${Math.floor(call.duration / 60)}:${(call.duration % 60).toString().padStart(2, '0')}` : '-'}</TableCell>
                  <TableCell>{new Date(call.created_at).toLocaleTimeString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

// Leads Management Component
function LeadsManagement() {
  const [leads, setLeads] = useState(mockLeads)
  const [selectedLead, setSelectedLead] = useState(null)
  const [isCallDialogOpen, setIsCallDialogOpen] = useState(false)

  const handleInitiateCall = async (leadId) => {
    try {
      // In a real app, this would make an API call
      console.log('Initiating call for lead:', leadId)
      setIsCallDialogOpen(false)
      // Show success message
    } catch (error) {
      console.error('Failed to initiate call:', error)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'new': return 'bg-blue-100 text-blue-800'
      case 'contacted': return 'bg-yellow-100 text-yellow-800'
      case 'qualified': return 'bg-green-100 text-green-800'
      case 'converted': return 'bg-purple-100 text-purple-800'
      case 'lost': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Lead Management</h1>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">
            <Upload className="w-4 h-4 mr-2" />
            Import CSV
          </Button>
          <Button size="sm">
            <UserPlus className="w-4 h-4 mr-2" />
            Add Lead
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Leads</CardTitle>
          <CardDescription>Manage and track your sales leads</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Company</TableHead>
                <TableHead>Industry</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Score</TableHead>
                <TableHead>Calls</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {leads.map((lead) => (
                <TableRow key={lead.id}>
                  <TableCell>
                    <div>
                      <div className="font-medium">{lead.name}</div>
                      <div className="text-sm text-muted-foreground">{lead.email}</div>
                    </div>
                  </TableCell>
                  <TableCell>{lead.company}</TableCell>
                  <TableCell>
                    <Badge variant="outline">{lead.industry}</Badge>
                  </TableCell>
                  <TableCell>
                    <Badge className={getStatusColor(lead.status)}>
                      {lead.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Progress value={lead.score} className="w-16" />
                      <span className="text-sm">{lead.score}</span>
                    </div>
                  </TableCell>
                  <TableCell>{lead.calls_count}</TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      <Dialog open={isCallDialogOpen} onOpenChange={setIsCallDialogOpen}>
                        <DialogTrigger asChild>
                          <Button 
                            size="sm" 
                            onClick={() => setSelectedLead(lead)}
                          >
                            <Phone className="w-4 h-4 mr-1" />
                            Call
                          </Button>
                        </DialogTrigger>
                        <DialogContent>
                          <DialogHeader>
                            <DialogTitle>Initiate Call</DialogTitle>
                            <DialogDescription>
                              Start an AI voice call to {selectedLead?.name} at {selectedLead?.company}
                            </DialogDescription>
                          </DialogHeader>
                          <div className="space-y-4">
                            <div>
                              <Label>Lead Information</Label>
                              <div className="mt-2 p-3 bg-muted rounded-md">
                                <p><strong>Name:</strong> {selectedLead?.name}</p>
                                <p><strong>Company:</strong> {selectedLead?.company}</p>
                                <p><strong>Phone:</strong> {selectedLead?.phone}</p>
                                <p><strong>Industry:</strong> {selectedLead?.industry}</p>
                              </div>
                            </div>
                            <div className="flex gap-2">
                              <Button 
                                onClick={() => handleInitiateCall(selectedLead?.id)}
                                className="flex-1"
                              >
                                <Play className="w-4 h-4 mr-2" />
                                Start Call
                              </Button>
                              <Button 
                                variant="outline" 
                                onClick={() => setIsCallDialogOpen(false)}
                                className="flex-1"
                              >
                                Cancel
                              </Button>
                            </div>
                          </div>
                        </DialogContent>
                      </Dialog>
                      <Button variant="outline" size="sm">
                        <FileText className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

// Call Monitor Component
function CallMonitor() {
  const [activeCalls, setActiveCalls] = useState([
    { id: 1, lead_name: 'David Chen', company: 'Chen Law Firm', status: 'in_progress', duration: 125, sentiment: 0.7 },
    { id: 2, lead_name: 'Lisa Martinez', company: 'Taco Fiesta', status: 'ringing', duration: 0, sentiment: 0 }
  ])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Live Call Monitor</h1>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">
            <Pause className="w-4 h-4 mr-2" />
            Pause All
          </Button>
          <Button size="sm">
            <Play className="w-4 h-4 mr-2" />
            Resume All
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {activeCalls.map((call) => (
          <Card key={call.id}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{call.lead_name}</CardTitle>
                <Badge variant={call.status === 'in_progress' ? 'default' : 'secondary'}>
                  {call.status}
                </Badge>
              </div>
              <CardDescription>{call.company}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Duration:</span>
                <span className="text-sm">
                  {call.duration > 0 ? `${Math.floor(call.duration / 60)}:${(call.duration % 60).toString().padStart(2, '0')}` : 'Not started'}
                </span>
              </div>
              
              {call.sentiment > 0 && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Sentiment:</span>
                    <span className="text-sm">
                      {call.sentiment > 0.6 ? 'Positive' : call.sentiment > 0.3 ? 'Neutral' : 'Negative'}
                    </span>
                  </div>
                  <Progress value={call.sentiment * 100} className="w-full" />
                </div>
              )}

              <div className="flex gap-2">
                <Button size="sm" variant="outline" className="flex-1">
                  <MessageSquare className="w-4 h-4 mr-2" />
                  Transcript
                </Button>
                <Button size="sm" variant="outline" className="flex-1">
                  <Settings className="w-4 h-4 mr-2" />
                  Control
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {activeCalls.length === 0 && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <PhoneCall className="w-12 h-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No Active Calls</h3>
            <p className="text-muted-foreground text-center">
              All AI agents are currently idle. Start a new call from the Leads page.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

// Analytics Component
function Analytics() {
  const performanceData = [
    { month: 'Jan', calls: 245, conversions: 58, revenue: 12400 },
    { month: 'Feb', calls: 289, conversions: 72, revenue: 15800 },
    { month: 'Mar', calls: 321, conversions: 89, revenue: 18900 },
    { month: 'Apr', calls: 298, conversions: 76, revenue: 16200 },
    { month: 'May', calls: 356, conversions: 98, revenue: 21500 },
    { month: 'Jun', calls: 378, conversions: 112, revenue: 24800 }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Analytics & Reports</h1>
        <div className="flex gap-2">
          <Select defaultValue="6months">
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1month">Last Month</SelectItem>
              <SelectItem value="3months">Last 3 Months</SelectItem>
              <SelectItem value="6months">Last 6 Months</SelectItem>
              <SelectItem value="1year">Last Year</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Performance Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$109,600</div>
            <p className="text-xs text-muted-foreground">+18% from last period</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">29.6%</div>
            <p className="text-xs text-muted-foreground">+3.2% from last period</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Deal Size</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$218</div>
            <p className="text-xs text-muted-foreground">-$12 from last period</p>
          </CardContent>
        </Card>
      </div>

      {/* Performance Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Performance Trends</CardTitle>
          <CardDescription>Monthly calls, conversions, and revenue over time</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Bar yAxisId="left" dataKey="calls" fill="#8884d8" name="Calls" />
              <Bar yAxisId="left" dataKey="conversions" fill="#82ca9d" name="Conversions" />
              <Line yAxisId="right" type="monotone" dataKey="revenue" stroke="#ff7300" name="Revenue ($)" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}

// Navigation Component
function Navigation() {
  const location = useLocation()
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: BarChart3 },
    { path: '/leads', label: 'Leads', icon: Users },
    { path: '/monitor', label: 'Live Monitor', icon: Activity },
    { path: '/analytics', label: 'Analytics', icon: TrendingUp },
  ]

  return (
    <nav className="bg-white border-r border-gray-200 w-64 min-h-screen p-4">
      <div className="mb-8">
        <h2 className="text-xl font-bold text-gray-800">AI Sales Agent</h2>
        <p className="text-sm text-gray-600">Voice Sales Dashboard</p>
      </div>
      
      <ul className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          
          return (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2 rounded-md transition-colors ${
                  isActive 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <Icon className="w-5 h-5" />
                {item.label}
              </Link>
            </li>
          )
        })}
      </ul>
    </nav>
  )
}

// Main App Component
function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-gray-50">
        <Navigation />
        <main className="flex-1 p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/leads" element={<LeadsManagement />} />
            <Route path="/monitor" element={<CallMonitor />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

