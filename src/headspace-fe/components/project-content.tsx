'use client'

import { useState, useEffect } from 'react'
import { ExternalLink, Github, Globe, Calendar, Tag, Cpu } from 'lucide-react'
import { projectsApi, Project } from '@/lib/api'
import { formatDate, formatCategory } from '@/lib/utils'

interface ProjectContentProps {
  projectId: string
}

export function ProjectContent({ projectId }: ProjectContentProps) {
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (projectId) {
      loadProject(projectId)
    }
  }, [projectId])

  const loadProject = async (id: string) => {
    try {
      setLoading(true)
      setError(null)
      const projectData = await projectsApi.getProject(id)
      setProject(projectData)
    } catch (err) {
      setError('Failed to load project details')
      console.error('Error loading project:', err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'completed':
        return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'archived':
        return 'bg-gray-100 text-gray-800 border-gray-200'
      case 'planning':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getLinkIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'github':
        return <Github className="w-4 h-4" />
      case 'demo':
      case 'live':
        return <Globe className="w-4 h-4" />
      default:
        return <ExternalLink className="w-4 h-4" />
    }
  }

  const getTechCategoryColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'frontend':
        return 'bg-blue-50 text-blue-700 border-blue-200'
      case 'backend':
        return 'bg-green-50 text-green-700 border-green-200'
      case 'database':
        return 'bg-purple-50 text-purple-700 border-purple-200'
      case 'devops':
        return 'bg-orange-50 text-orange-700 border-orange-200'
      case 'ml':
      case 'ai':
        return 'bg-pink-50 text-pink-700 border-pink-200'
      default:
        return 'bg-gray-50 text-gray-700 border-gray-200'
    }
  }

  if (loading) {
    return (
      <div className="flex-1 p-8">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="space-y-2">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            <div className="h-4 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex-1 p-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="text-red-800 font-medium">Error</div>
          <div className="text-red-600 text-sm mt-1">{error}</div>
          <button 
            onClick={() => loadProject(projectId)}
            className="mt-3 text-red-600 hover:text-red-800 text-sm underline"
          >
            Try again
          </button>
        </div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="flex-1 p-8 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-500 text-lg mb-2">Select a project</div>
          <div className="text-gray-400 text-sm">Choose a project from the sidebar to view details</div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-4xl mx-auto p-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <h1 className="text-3xl font-bold text-gray-900">{project.title}</h1>
              <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(project.status)}`}>
                {project.status}
              </span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Calendar className="w-4 h-4" />
              <span>Updated {formatDate(project.updated_at)}</span>
            </div>
          </div>
          
          <p className="text-lg text-gray-600 mb-4">{project.short_description}</p>
          
          <div className="flex items-center space-x-4 mb-6">
            <span className="text-sm font-medium text-gray-700">Category:</span>
            <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm">
              {formatCategory(project.category)}
            </span>
          </div>

          {/* Project Image */}
          {project.image_url && (
            <div className="mb-6">
              <img
                src={project.image_url}
                alt={project.title}
                className="w-full h-64 object-cover rounded-lg border border-gray-200"
              />
            </div>
          )}

          {/* Links */}
          {project.links.length > 0 && (
            <div className="flex flex-wrap gap-3 mb-6">
              {project.links.map((link, index) => (
                <a
                  key={index}
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors border border-blue-200"
                >
                  {getLinkIcon(link.type)}
                  <span className="text-sm font-medium">{link.title}</span>
                </a>
              ))}
            </div>
          )}
        </div>

        {/* Content Sections */}
        <div className="space-y-8">
          {/* Overview */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Overview</h2>
            <div className="prose prose-lg max-w-none">
              <p className="text-gray-700 leading-relaxed">{project.content.overview}</p>
            </div>
          </section>

          {/* Features */}
          {project.content.features.length > 0 && (
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Key Features</h2>
              <ul className="space-y-2">
                {project.content.features.map((feature, index) => (
                  <li key={index} className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Technologies */}
          {project.technologies.length > 0 && (
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Technologies</h2>
              <div className="space-y-4">
                {Object.entries(
                  project.technologies.reduce((acc, tech) => {
                    const category = tech.category || 'other'
                    if (!acc[category]) acc[category] = []
                    acc[category].push(tech)
                    return acc
                  }, {} as Record<string, typeof project.technologies>)
                ).map(([category, techs]) => (
                  <div key={category}>
                    <h3 className="text-sm font-medium text-gray-900 mb-2 capitalize">
                      <div className="flex items-center space-x-2">
                        <Cpu className="w-4 h-4" />
                        <span>{category}</span>
                      </div>
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {techs.map((tech, index) => (
                        <span
                          key={index}
                          className={`px-3 py-1 rounded-full text-sm font-medium border ${getTechCategoryColor(category)}`}
                        >
                          {tech.name}
                          {tech.version && (
                            <span className="text-xs opacity-75 ml-1">v{tech.version}</span>
                          )}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Technical Details */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Technical Details</h2>
            <div className="prose prose-lg max-w-none">
              <p className="text-gray-700 leading-relaxed">{project.content.technical_details}</p>
            </div>
          </section>

          {/* Challenges */}
          {project.content.challenges && (
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Challenges</h2>
              <div className="prose prose-lg max-w-none">
                <p className="text-gray-700 leading-relaxed">{project.content.challenges}</p>
              </div>
            </section>
          )}

          {/* Learnings */}
          {project.content.learnings && (
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Key Learnings</h2>
              <div className="prose prose-lg max-w-none">
                <p className="text-gray-700 leading-relaxed">{project.content.learnings}</p>
              </div>
            </section>
          )}

          {/* Next Steps */}
          {project.content.next_steps && (
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Next Steps</h2>
              <div className="prose prose-lg max-w-none">
                <p className="text-gray-700 leading-relaxed">{project.content.next_steps}</p>
              </div>
            </section>
          )}

          {/* Tags */}
          {project.tags.length > 0 && (
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Tags</h2>
              <div className="flex flex-wrap gap-2">
                {project.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center space-x-1 px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                  >
                    <Tag className="w-3 h-3" />
                    <span>{tag}</span>
                  </span>
                ))}
              </div>
            </section>
          )}
        </div>
      </div>
    </div>
  )
} 