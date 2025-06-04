# Headspace – Project Portfolio

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)](https://nodejs.org/)

A modern, responsive portfolio application to help developers organize and showcase their projects. Built with **FastAPI** (backend), **Next.js** (frontend), and **shadcn/ui** components for a beautiful, intuitive user experience.

The goal is to help its ADHD coder to cope with a lot of information.

---

## 🏗️ Architecture

- **Backend:** FastAPI, Pydantic, UV (Python package manager)
- **Frontend:** Next.js 14, TypeScript, shadcn/ui, Tailwind CSS
- **API Communication:** Axios with SWR
- **Styling:** Tailwind CSS, custom shadcn/ui components

## 📁 Project Structure

```
├── src/
│   ├── headspace-be/          # Backend (FastAPI + Pydantic)
│   │   ├── pyproject.toml     # UV configuration
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── models.py          # Pydantic data models
│   │   ├── routes.py          # API routes
│   │   └── projects_data.json # Project data storage
│   └── headspace-fe/          # Frontend (Next.js + shadcn/ui)
│       ├── package.json       # Node.js dependencies
│       ├── app/               # Next.js App Router
│       ├── components/        # React components
│       └── lib/               # Utilities and API client
├── README.md
└── .gitignore
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- [UV](https://github.com/astral-sh/uv) (Python package manager)

### Backend Setup

```bash
cd src/headspace-be
uv pip install -e .
uv run python main.py
```
- API: http://localhost:8000
- Docs: http://localhost:8000/api/docs
- Health: http://localhost:8000/health

### Frontend Setup

```bash
cd src/headspace-fe
npm install
npm run dev
```
- Frontend: http://localhost:3000

## 🎯 Features

### Backend
- Modern FastAPI framework with automatic API docs
- Pydantic models for type-safe validation
- CORS support for frontend integration
- RESTful API: full CRUD for projects
- Filtering by category, status, tags, and search
- Sample data included

### Frontend
- Responsive design for desktop and mobile
- Sidebar navigation with collapsible categories
- Dynamic project details (no page reload)
- Modern UI with shadcn/ui and Tailwind CSS
- TypeScript for type safety
- Loading and error states
- Visual project status indicators

### Project Data Model
Each project includes:
- **Basic Info:** Title, description, category, status
- **Content:** Overview, features, technical details, challenges, learnings
- **Technologies:** Categorized tech stack with versions
- **Links:** GitHub, demo, documentation
- **Metadata:** Tags, priority, timestamps, images

## 🎨 UI Components
- **Card:** Project display
- **Button:** Interactive elements
- **Icons:** Lucide React icons
- **Navigation:** Sidebar with collapsible sections
- **Status Indicators:** Color-coded project status

## 📱 Responsive Design
- **Desktop:** Full sidebar, detailed info
- **Mobile:** Collapsible sidebar, optimized layout
- **Smooth transitions:** Enhanced UX

## 🔧 Development

### Backend
```bash
cd src/headspace-be
uv run python main.py  # Hot reload
```

### Frontend
```bash
cd src/headspace-fe
npm run dev           # Dev server
npm run build         # Production build
npm run type-check    # TypeScript check
```

### Production Build

1. Build frontend:
   ```bash
   cd src/headspace-fe
   npm run build
   ```
2. Serve built frontend with FastAPI backend

## 🌟 Customization

### Add Projects
- Edit `src/headspace-be/projects_data.json`
- Use API endpoints
- Update sample data in `routes.py`

### Styling
- Edit `src/headspace-fe/app/globals.css` for global styles
- Update `tailwind.config.js` for theme
- Customize shadcn/ui in `components/ui/`

### Add Categories
- Update `ProjectCategory` enum in `src/headspace-be/models.py`

## 📚 API Documentation

Interactive docs: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

**Key Endpoints:**
- `GET /api/projects` – List/filter projects
- `GET /api/projects/{id}` – Project details
- `POST /api/projects` – Create project
- `PUT /api/projects/{id}` – Update project
- `DELETE /api/projects/{id}` – Delete project

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test backend and frontend
5. Submit a pull request

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

Built with ❤️ using FastAPI, Next.js, and shadcn/ui.

## 📬 Contact

For questions, suggestions, or support, please open an issue or contact the maintainer at [your-email@example.com]. # headspace
