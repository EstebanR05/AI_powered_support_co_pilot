# 🚀 AI-Powered Support Co-Pilot

> **Revolutionizing Customer Experience with Real-Time Artificial Intelligence.**

Welcome to the **AI-Powered Support Co-Pilot** frontend. This is not just a dashboard; it is a cutting-edge visualization interface designed to empower support teams with god-like visibility into their operations using advanced Generative AI and real-time data streams.

Built for the modern web, this application connects seamlessly with our intelligent backend ecosystem to render categorized, sentiment-analyzed support tickets the instant they arrive—no page refreshes required.

## ✨ Key Features

- **⚡ Real-Time Telemetry**: Leveraging Supabase Realtime channels to push updates instantly. Watch tickets appear and evolve live.
- **🧠 AI-Driven Insights**: Visualization of Sentiment Analysis (Positive, Neutral, Negative) and Smart Categorization powered by our dedicated LLM microservice.
- **🎨 Modern Aesthetic**: A clean, high-performance UI built with Tailwind CSS, designed for clarity and speed.
- **🛡️ Type-Safe Architecture**: Robust development with TypeScript ensuring reliability and scalability.

## 🛠️ Technology Stack

- **Framework**: React 18 + Vite (Lightning fast HMR)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Data & Realtime**: Supabase Client
- **Runtime & Package Manager**: Bun

## 🚀 Getting Started

This project utilizes [Bun](https://bun.sh) for ultra-fast dependency management and script execution.

### Prerequisites

Ensure you have **Bun** installed on your machine:

```bash
curl -fsSL https://bun.sh/install | bash
```

### Installation

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
bun install
```

### Configuration

Create a `.env` file in the root of the `frontend` directory with your Supabase credentials:

```bash
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### Development

Start the high-performance development server:

```bash
bun run dev
```

The application will be available at `http://localhost:5173`.

### Production Build

Generate the optimized production build:

```bash
bun run build
```

---

*Built with ❤️ by the AI-Powered Support Co-Pilot Team.*