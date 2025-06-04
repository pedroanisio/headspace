'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/sidebar'
import { ProjectContent } from '@/components/project-content'

export default function HomePage() {
  const [selectedProjectId, setSelectedProjectId] = useState<string | undefined>()

  const handleProjectSelect = (projectId: string) => {
    setSelectedProjectId(projectId)
  }

  return (
    <div className="h-screen flex bg-white">
      <Sidebar 
        selectedProjectId={selectedProjectId}
        onProjectSelect={handleProjectSelect}
      />
      <div className="flex-1 flex flex-col min-w-0">
        {selectedProjectId ? (
          <ProjectContent projectId={selectedProjectId} />
        ) : (
          <div className="flex-1 flex items-center justify-center bg-gray-50">
            <div className="text-center">
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Welcome to Headspace
              </h2>
              <p className="text-gray-600 mb-6 max-w-md">
                Select a project from the sidebar to explore my work and see detailed information about each project.
              </p>
              <div className="grid grid-cols-2 gap-4 text-sm text-gray-500">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>Active Projects</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span>Completed</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                  <span>In Planning</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-gray-500 rounded-full"></div>
                  <span>Archived</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
} 