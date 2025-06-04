'use client'

import { useState, useEffect } from 'react'
import { ChevronDown, ChevronRight, FolderOpen, Folder, FileText, Settings, Code2, BookOpen, Search, Bookmark, StickyNote } from 'lucide-react'
import { projectsApi, ProjectSummary } from '@/lib/api'
import { formatCategory } from '@/lib/utils'

interface SidebarProps {
  selectedProjectId?: string
  onProjectSelect: (projectId: string) => void
}

interface GroupedProjects {
  [category: string]: ProjectSummary[]
}

type NavigationSection = 'settings' | 'codespace' | 'blog' | 'research' | 'bookmarks' | 'notes'

export function Sidebar({ selectedProjectId, onProjectSelect }: SidebarProps) {
  const [projects, setProjects] = useState<ProjectSummary[]>([])
  const [groupedProjects, setGroupedProjects] = useState<GroupedProjects>({})
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set())
  const [expandedSections, setExpandedSections] = useState<Set<NavigationSection>>(new Set<NavigationSection>(['codespace']))
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    try {
      setLoading(true)
      const response = await projectsApi.getProjects()
      setProjects(response.projects)
      
      // Group projects by category
      const grouped = response.projects.reduce((acc, project) => {
        const category = project.category
        if (!acc[category]) {
          acc[category] = []
        }
        acc[category].push(project)
        return acc
      }, {} as GroupedProjects)
      
      setGroupedProjects(grouped)
      
      // Expand categories that have projects by default
      setExpandedCategories(new Set(Object.keys(grouped)))
    } catch (err) {
      setError('Failed to load projects')
      console.error('Error loading projects:', err)
    } finally {
      setLoading(false)
    }
  }

  const toggleSection = (section: NavigationSection) => {
    const newExpanded = new Set(expandedSections)
    if (newExpanded.has(section)) {
      newExpanded.delete(section)
    } else {
      newExpanded.add(section)
    }
    setExpandedSections(newExpanded)
  }

  const toggleCategory = (category: string) => {
    const newExpanded = new Set(expandedCategories)
    if (newExpanded.has(category)) {
      newExpanded.delete(category)
    } else {
      newExpanded.add(category)
    }
    setExpandedCategories(newExpanded)
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <div className="w-2 h-2 bg-green-500 rounded-full" />
      case 'completed':
        return <div className="w-2 h-2 bg-blue-500 rounded-full" />
      case 'archived':
        return <div className="w-2 h-2 bg-gray-500 rounded-full" />
      case 'planning':
        return <div className="w-2 h-2 bg-yellow-500 rounded-full" />
      default:
        return <div className="w-2 h-2 bg-gray-300 rounded-full" />
    }
  }

  if (loading) {
    return (
      <div className="w-80 bg-slate-50 border-r border-slate-200 p-4">
        <div className="animate-pulse">
          <div className="h-8 bg-slate-200 rounded mb-4"></div>
          <div className="space-y-2">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-6 bg-slate-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="w-80 bg-slate-50 border-r border-slate-200 p-4">
        <div className="text-red-600 text-sm">{error}</div>
        <button 
          onClick={loadProjects}
          className="mt-2 text-blue-600 hover:text-blue-800 text-sm underline"
        >
          Try again
        </button>
      </div>
    )
  }

  return (
    <div className="w-80 bg-slate-50 border-r border-slate-200 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-slate-200">
        <h1 className="text-xl font-bold text-slate-900">Headspace</h1>
        <p className="text-sm text-slate-600 mt-1">Project Portfolio</p>
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-4">
          <div className="space-y-2">
            
            {/* Settings Section */}
            <div>
              <button
                onClick={() => toggleSection('settings')}
                className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-100 rounded-md transition-colors border-b border-slate-200"
              >
                <div className="flex items-center space-x-3">
                  <Settings className="w-5 h-5 text-slate-600" />
                  <span className="text-sm font-semibold text-slate-700">
                    Settings
                  </span>
                </div>
                {expandedSections.has('settings') ? (
                  <ChevronDown className="w-4 h-4 text-slate-400" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-slate-400" />
                )}
              </button>

              {/* Settings Content */}
              {expandedSections.has('settings') && (
                <div className="ml-8 mt-2 space-y-1">
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Profile Settings
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Preferences
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Account
                  </button>
                </div>
              )}
            </div>

            {/* Blog Section */}
            <div>
              <button
                onClick={() => toggleSection('blog')}
                className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-100 rounded-md transition-colors border-b border-slate-200"
              >
                <div className="flex items-center space-x-3">
                  <BookOpen className="w-5 h-5 text-slate-600" />
                  <span className="text-sm font-semibold text-slate-700">
                    Blog
                  </span>
                </div>
                {expandedSections.has('blog') ? (
                  <ChevronDown className="w-4 h-4 text-slate-400" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-slate-400" />
                )}
              </button>

              {/* Blog Content */}
              {expandedSections.has('blog') && (
                <div className="ml-8 mt-2 space-y-1">
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    All Posts
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Drafts
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Categories
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Tags
                  </button>
                </div>
              )}
            </div>

            {/* Research Section */}
            <div>
              <button
                onClick={() => toggleSection('research')}
                className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-100 rounded-md transition-colors border-b border-slate-200"
              >
                <div className="flex items-center space-x-3">
                  <Search className="w-5 h-5 text-slate-600" />
                  <span className="text-sm font-semibold text-slate-700">
                    Research
                  </span>
                </div>
                {expandedSections.has('research') ? (
                  <ChevronDown className="w-4 h-4 text-slate-400" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-slate-400" />
                )}
              </button>

              {/* Research Content */}
              {expandedSections.has('research') && (
                <div className="ml-8 mt-2 space-y-1">
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Papers
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Research Notes
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    References
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Bibliography
                  </button>
                </div>
              )}
            </div>

            {/* Bookmarks Section */}
            <div>
              <button
                onClick={() => toggleSection('bookmarks')}
                className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-100 rounded-md transition-colors border-b border-slate-200"
              >
                <div className="flex items-center space-x-3">
                  <Bookmark className="w-5 h-5 text-slate-600" />
                  <span className="text-sm font-semibold text-slate-700">
                    Bookmarks
                  </span>
                </div>
                {expandedSections.has('bookmarks') ? (
                  <ChevronDown className="w-4 h-4 text-slate-400" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-slate-400" />
                )}
              </button>

              {/* Bookmarks Content */}
              {expandedSections.has('bookmarks') && (
                <div className="ml-8 mt-2 space-y-1">
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    All Bookmarks
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Development
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Design
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Articles
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Tools
                  </button>
                </div>
              )}
            </div>

            {/* Notes Section */}
            <div>
              <button
                onClick={() => toggleSection('notes')}
                className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-100 rounded-md transition-colors border-b border-slate-200"
              >
                <div className="flex items-center space-x-3">
                  <StickyNote className="w-5 h-5 text-slate-600" />
                  <span className="text-sm font-semibold text-slate-700">
                    Notes
                  </span>
                </div>
                {expandedSections.has('notes') ? (
                  <ChevronDown className="w-4 h-4 text-slate-400" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-slate-400" />
                )}
              </button>

              {/* Notes Content */}
              {expandedSections.has('notes') && (
                <div className="ml-8 mt-2 space-y-1">
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Quick Notes
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Meeting Notes
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Ideas
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    To-Do Lists
                  </button>
                  <button className="w-full text-left p-2 text-sm text-slate-600 hover:bg-slate-100 rounded">
                    Archive
                  </button>
                </div>
              )}
            </div>

            {/* Codespace Section */}
            <div>
              <button
                onClick={() => toggleSection('codespace')}
                className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-100 rounded-md transition-colors border-b border-slate-200"
              >
                <div className="flex items-center space-x-3">
                  <Code2 className="w-5 h-5 text-slate-600" />
                  <span className="text-sm font-semibold text-slate-700">
                    Codespace
                  </span>
                  <span className="text-xs text-slate-500 bg-slate-200 px-2 py-0.5 rounded-full">
                    {projects.length}
                  </span>
                </div>
                {expandedSections.has('codespace') ? (
                  <ChevronDown className="w-4 h-4 text-slate-400" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-slate-400" />
                )}
              </button>

              {/* Codespace Content - Categories and Projects */}
              {expandedSections.has('codespace') && (
                <div className="ml-6 mt-2 space-y-1">
                  {Object.entries(groupedProjects).map(([category, categoryProjects]) => (
                    <div key={category}>
                      {/* Category Header */}
                      <button
                        onClick={() => toggleCategory(category)}
                        className="w-full flex items-center justify-between p-2 text-left hover:bg-slate-100 rounded-md transition-colors"
                      >
                        <div className="flex items-center space-x-2">
                          {expandedCategories.has(category) ? (
                            <FolderOpen className="w-4 h-4 text-slate-600" />
                          ) : (
                            <Folder className="w-4 h-4 text-slate-600" />
                          )}
                          <span className="text-sm font-medium text-slate-700">
                            {formatCategory(category)}
                          </span>
                          <span className="text-xs text-slate-500 bg-slate-200 px-2 py-0.5 rounded-full">
                            {categoryProjects.length}
                          </span>
                        </div>
                        {expandedCategories.has(category) ? (
                          <ChevronDown className="w-4 h-4 text-slate-400" />
                        ) : (
                          <ChevronRight className="w-4 h-4 text-slate-400" />
                        )}
                      </button>

                      {/* Projects List */}
                      {expandedCategories.has(category) && (
                        <div className="ml-6 mt-1 space-y-1">
                          {categoryProjects
                            .sort((a, b) => b.priority - a.priority || a.title.localeCompare(b.title))
                            .map((project) => (
                              <button
                                key={project.id}
                                onClick={() => onProjectSelect(project.id)}
                                className={`w-full flex items-center space-x-2 p-2 text-left rounded-md transition-colors ${
                                  selectedProjectId === project.id
                                    ? 'bg-blue-100 text-blue-900 border border-blue-200'
                                    : 'hover:bg-slate-100 text-slate-700'
                                }`}
                              >
                                <FileText className="w-3 h-3 flex-shrink-0" />
                                <div className="flex-1 min-w-0">
                                  <div className="text-sm font-medium truncate">
                                    {project.title}
                                  </div>
                                  <div className="text-xs text-slate-500 truncate">
                                    {project.short_description}
                                  </div>
                                </div>
                                <div className="flex items-center space-x-1 flex-shrink-0">
                                  {getStatusIcon(project.status)}
                                </div>
                              </button>
                            ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-slate-200">
        <div className="text-xs text-slate-500 text-center">
          {projects.length} projects total
        </div>
      </div>
    </div>
  )
} 