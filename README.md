<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Muzaffar Developers | Full-Stack, Mobile & Desktop Solutions</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        cyanAccent: '#06b6d4',
                        indigoAccent: '#6366f1',
                        darkBg: '#0b0f19',
                        cardBg: 'rgba(17, 24, 39, 0.7)',
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                    animation: {
                        'pulse-glow': 'pulseGlow 4s infinite alternate',
                        'float': 'float 6s ease-in-out infinite',
                    },
                    keyframes: {
                        pulseGlow: {
                            '0%': { opacity: '0.4', filter: 'blur(40px)' },
                            '100%': { opacity: '0.8', filter: 'blur(60px)' },
                        },
                        float: {
                            '0%, 100%': { transform: 'translateY(0px)' },
                            '50%': { transform: 'translateY(-10px)' },
                        }
                    }
                }
            }
        }
    </script>
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0b0f19;
            color: #f3f4f6;
            overflow-x: hidden;
        }
        .glass-card {
            background: rgba(17, 24, 39, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glass-card:hover {
            border-color: rgba(6, 182, 212, 0.4);
            box-shadow: 0 10px 30px -10px rgba(6, 182, 212, 0.2);
        }
        .glass-nav {
            background: rgba(11, 15, 25, 0.8);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .text-gradient {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .bg-gradient-btn {
            background: linear-gradient(135deg, #06b6d4 0%, #4f46e5 100%);
        }
        .bg-gradient-btn:hover {
            background: linear-gradient(135deg, #0891b2 0%, #4338ca 100%);
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0b0f19;
        }
        ::-webkit-scrollbar-thumb {
            background: #1f2937;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #06b6d4;
        }
    </style>
</head>
<body class="antialiased selection:bg-cyan-500 selection:text-white">

    <!-- Navigation Header -->
    <header class="fixed top-0 left-0 w-full z-50 glass-nav transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-20">
                <!-- Logo -->
                <a href="#" class="flex items-center gap-3 group">
                    <div class="w-10 h-10 rounded-xl bg-gradient-btn flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform duration-300">
                        M
                    </div>
                    <div>
                        <span class="text-xl font-bold tracking-tight text-white group-hover:text-cyan-400 transition-colors">Muzaffar</span>
                        <span class="text-xl font-light text-cyan-400">Developers</span>
                    </div>
                </a>

                <!-- Desktop Nav Navigation -->
                <nav class="hidden md:flex items-center space-x-8">
                    <a href="#about" class="text-sm font-medium text-gray-300 hover:text-cyan-400 transition-colors">About</a>
                    <a href="#services" class="text-sm font-medium text-gray-300 hover:text-cyan-400 transition-colors">Services</a>
                    <a href="#projects" class="text-sm font-medium text-gray-300 hover:text-cyan-400 transition-colors">Projects</a>
                    <a href="#github-guide" class="text-sm font-medium text-gray-300 hover:text-cyan-400 transition-colors">Deployment</a>
                    <a href="#contact" class="px-5 py-2.5 rounded-full bg-gradient-btn text-white text-sm font-semibold shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40 hover:scale-105 transition-all">
                        Contact Me
                    </a>
                </nav>

                <!-- Mobile Menu Button -->
                <div class="md:hidden">
                    <button id="mobile-menu-btn" class="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 focus:outline-none">
                        <i class="fa-solid fa-bars text-xl"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Navigation Menu -->
        <div id="mobile-menu" class="hidden md:hidden glass-card border-b border-gray-800 px-4 pt-2 pb-6 space-y-3">
            <a href="#about" class="mobile-link block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-800">About</a>
            <a href="#services" class="mobile-link block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-800">Services</a>
            <a href="#projects" class="mobile-link block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-800">Projects</a>
            <a href="#github-guide" class="mobile-link block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-800">Deployment</a>
            <a href="#contact" class="mobile-link block px-3 py-2 rounded-md text-base font-medium text-center bg-gradient-btn text-white shadow-lg">Contact Me</a>
        </div>
    </header>

    <!-- Background Ambient Glow -->
    <div class="fixed top-20 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full animate-pulse-glow pointer-events-none -z-10"></div>
    <div class="fixed top-1/2 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full animate-pulse-glow pointer-events-none -z-10" style="animation-delay: 2s;"></div>

    <!-- Hero Section -->
    <section class="min-h-screen pt-32 pb-20 flex items-center justify-center relative px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div class="max-w-5xl mx-auto text-center space-y-8">
            <!-- Badge -->
            <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card border border-cyan-500/30 text-cyan-300 text-xs sm:text-sm font-medium animate-float">
                <span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
                Available for Desktop, Web & Mobile Projects
            </div>

            <!-- Title -->
            <h1 class="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white leading-tight">
                Architecting High-Performance <br class="hidden sm:inline"/>
                <span class="text-gradient">Software & Digital Solutions</span>
            </h1>

            <!-- Subtitle -->
            <p class="max-w-3xl mx-auto text-lg sm:text-xl text-gray-400 font-normal leading-relaxed">
                Welcome to <strong class="text-white font-semibold">Muzaffar Developers</strong>. We build custom Python desktop applications, modern web apps with FastAPI & Flask, cross-platform Flutter mobile apps, automated data systems, and sleek UI/UX visual experiences.
            </p>

            <!-- Call to Actions -->
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                <a href="#projects" class="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-btn text-white font-semibold shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:scale-105 transition-all flex items-center justify-center gap-2">
                    <span>Explore Showcase</span>
                    <i class="fa-solid fa-arrow-right text-sm"></i>
                </a>
                <a href="#contact" class="w-full sm:w-auto px-8 py-4 rounded-xl glass-card text-gray-300 font-semibold hover:text-white hover:bg-gray-800/80 transition-all border border-gray-700 flex items-center justify-center gap-2">
                    <i class="fa-regular fa-paper-plane text-cyan-400"></i>
                    <span>Get in Touch</span>
                </a>
            </div>

            <!-- Quick Metrics / Tech Badges -->
            <div class="pt-12 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
                <div class="glass-card p-4 rounded-2xl">
                    <p class="text-3xl font-extrabold text-cyan-400">100%</p>
                    <p class="text-xs text-gray-400 mt-1">Custom Architecture</p>
                </div>
                <div class="glass-card p-4 rounded-2xl">
                    <p class="text-3xl font-extrabold text-indigo-400">Cross-Platform</p>
                    <p class="text-xs text-gray-400 mt-1">Desktop & Mobile</p>
                </div>
                <div class="glass-card p-4 rounded-2xl">
                    <p class="text-3xl font-extrabold text-cyan-400">FastAPI / Flask</p>
                    <p class="text-xs text-gray-400 mt-1">Lightweight Backends</p>
                </div>
                <div class="glass-card p-4 rounded-2xl">
                    <p class="text-3xl font-extrabold text-indigo-400">Automated</p>
                    <p class="text-xs text-gray-400 mt-1">Data Pipelines</p>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-24 relative px-4 sm:px-6 lg:px-8 border-t border-gray-800/50">
        <div class="max-w-7xl mx-auto">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
                <!-- Text Column -->
                <div class="lg:col-span-7 space-y-6">
                    <div class="inline-flex items-center gap-2 text-cyan-400 font-semibold text-sm tracking-wider uppercase">
                        <i class="fa-solid fa-code"></i> About Muzaffar Developers
                    </div>
                    <h2 class="text-3xl sm:text-4xl font-bold text-white">
                        Bridging Complex Logic with Elegant Visual Design
                    </h2>
                    <p class="text-gray-300 leading-relaxed">
                        At <strong class="text-white">Muzaffar Developers</strong>, we specialize in solving real-world challenges through full-stack software development. From high-throughput desktop management applications with Python and SQLite to reactive mobile applications built on Flutter and Supabase, we focus on efficiency, clarity, and reliability.
                    </p>
                    <p class="text-gray-400 leading-relaxed">
                        Whether automating complex Excel workflows with Power Query and PySerial integration, or creating Figma UI/UX wireframes and 3D architectural visual designs, our work combines clean engineering with modern visual appeal.
                    </p>

                    <!-- Core Technologies Pill Cloud -->
                    <div class="pt-4">
                        <h3 class="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-3">Core Tech Stack</h3>
                        <div class="flex flex-wrap gap-2">
                            <span class="px-3 py-1.5 rounded-lg bg-gray-800/80 border border-gray-700 text-xs font-medium text-cyan-300"><i class="fa-brands fa-python text-yellow-400 mr-1"></i> Python</span>
                            <span class="px-3 py-1.5 rounded-lg bg-gray-800/80 border border-gray-700 text-xs font-medium text-indigo-300"><i class="fa-solid fa-desktop mr-1"></i> Tkinter / CustomTkinter</span>
                            <span class="px-3 py-1.5 rounded-lg bg-gray-800/80 border border-gray-700 text-xs font-medium text-cyan-300"><i class="fa-solid fa-bolt mr-1"></i> FastAPI</span>
                            <span class="px-3 py-1.5 rounded-lg bg-gray-800/80 border border-gray-700 text-xs font-medium text-indigo-300"><i class="fa-solid fa-flask mr-1"></i> Flask</span>
                            <span class="px-3 py-1.5 rounded-lg bg-gray-800/80 border border-gray-700 text-xs font-medium text-cyan-300"><i class="fa-solid fa-mobile-screen mr-1"></i> Flutter</span>
                            <span class="px-3 py-1.5 rounded-lg bg-gray-800/80 border border-gray-700 text-xs font-medium text-indigo-300"><i class="fa-solid fa-database mr-1"></i> Supabase & SQLite</span>
                            <span class="px-3 py-1.5 rounded-lg bg-gray-800/80 border border-gray-700 text-xs font-medium text-cyan-300"><i class="fa-file-excel text-green-400 mr-1"></i> Excel Power Query</span>
                            <span class="px-3 py-1.5 rounded-lg bg-gray-800/80 border border-gray-700 text-xs font-medium text-indigo-300"><i class="fa-brands fa-figma text-pink-400 mr-1"></i> Figma UI/UX</span>
                            <span class="px-3 py-1.5 rounded-lg bg-gray-800/80 border border-gray-700 text-xs font-medium text-cyan-300"><i class="fa-solid fa-cubes mr-1"></i> 3D Architectural Visuals</span>
                        </div>
                    </div>
                </div>

                <!-- Code / Feature Highlight Card Column -->
                <div class="lg:col-span-5">
                    <div class="glass-card rounded-2xl p-6 relative overflow-hidden group border border-gray-700">
                        <!-- Top Bar Decor -->
                        <div class="flex items-center justify-between pb-4 border-b border-gray-800">
                            <div class="flex space-x-2">
                                <div class="w-3 h-3 rounded-full bg-red-500/80"></div>
                                <div class="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                                <div class="w-3 h-3 rounded-full bg-green-500/80"></div>
                            </div>
                            <span class="text-xs text-gray-500 font-mono">muzaffar_dev_core.py</span>
                        </div>
                        <!-- Snippet View -->
                        <pre class="mt-4 text-xs sm:text-sm font-mono text-gray-300 leading-relaxed overflow-x-auto">
<span class="text-purple-400">class</span> <span class="text-yellow-300">MuzaffarDeveloper</span>:
    <span class="text-purple-400">def</span> <span class="text-blue-400">__init__</span>(self):
        self.focus = <span class="text-green-300">"Robust Software & Modern Design"</span>
        self.skills = [
            <span class="text-green-300">"Python ERPs"</span>, <span class="text-green-300">"FastAPI Backends"</span>,
            <span class="text-green-300">"Flutter Apps"</span>, <span class="text-green-300">"Data Scraping"</span>
        ]

    <span class="text-purple-400">def</span> <span class="text-blue-400">deliver_solution</span>(self, requirements):
        <span class="text-purple-400">return</span> {
            <span class="text-green-300">"status"</span>: <span class="text-cyan-300">"Optimized & Scalable"</span>,
            <span class="text-green-300">"design"</span>: <span class="text-cyan-300">"Modern Glassmorphism UI"</span>,
            <span class="text-green-300">"ready"</span>: <span class="text-cyan-300">True</span>
        }
                        </pre>
                        <!-- Bottom Info -->
                        <div class="mt-6 pt-4 border-t border-gray-800 flex items-center justify-between text-xs text-gray-400">
                            <span class="flex items-center gap-2"><i class="fa-solid fa-check text-green-400"></i> Clean Architecture</span>
                            <span class="flex items-center gap-2"><i class="fa-solid fa-check text-green-400"></i> Cross-Platform Deployment</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Grid Section -->
    <section id="services" class="py-24 relative px-4 sm:px-6 lg:px-8 bg-gray-950/40 border-t border-gray-800/50">
        <div class="max-w-7xl mx-auto">
            <!-- Header -->
            <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
                <div class="inline-flex items-center gap-2 text-cyan-400 font-semibold text-sm tracking-wider uppercase">
                    <i class="fa-solid fa-gears"></i> Tailored Solutions
                </div>
                <h2 class="text-3xl sm:text-5xl font-extrabold text-white">
                    Services We Provide
                </h2>
                <p class="text-gray-400 text-base sm:text-lg">
                    End-to-end development tailored for businesses, startups, and operational productivity.
                </p>
            </div>

            <!-- Cards Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

                <!-- Service 1 -->
                <div class="glass-card rounded-2xl p-8 transition-all duration-300 hover:-translate-y-2 relative group">
                    <div class="w-14 h-14 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
                        <i class="fa-solid fa-laptop-code"></i>
                    </div>
                    <h3 class="text-xl font-bold text-white mb-3">Desktop & ERP Applications</h3>
                    <p class="text-gray-400 text-sm leading-relaxed mb-4">
                        Custom standalone desktop software, inventory tools, point-of-sale systems, and hardware integrations (PySerial, barcode scanners) using Python, Tkinter, and SQLite.
                    </p>
                    <ul class="text-xs text-gray-400 space-y-2 border-t border-gray-800 pt-4">
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-cyan-400"></i> Local SQLite / Database Sync</li>
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-cyan-400"></i> Hardware/Serial Port Communication</li>
                    </ul>
                </div>

                <!-- Service 2 -->
                <div class="glass-card rounded-2xl p-8 transition-all duration-300 hover:-translate-y-2 relative group">
                    <div class="w-14 h-14 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
                        <i class="fa-solid fa-globe"></i>
                    </div>
                    <h3 class="text-xl font-bold text-white mb-3">Web Development & APIs</h3>
                    <p class="text-gray-400 text-sm leading-relaxed mb-4">
                        High-performance REST APIs and responsive web portals built using FastAPI, Flask, HTMX, HTML5, and Tailwind CSS with fast loading speed and sleek layouts.
                    </p>
                    <ul class="text-xs text-gray-400 space-y-2 border-t border-gray-800 pt-4">
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-indigo-400"></i> FastAPI / Flask Backends</li>
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-indigo-400"></i> Responsive Single-Page Layouts</li>
                    </ul>
                </div>

                <!-- Service 3 -->
                <div class="glass-card rounded-2xl p-8 transition-all duration-300 hover:-translate-y-2 relative group">
                    <div class="w-14 h-14 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
                        <i class="fa-solid fa-mobile-screen-button"></i>
                    </div>
                    <h3 class="text-xl font-bold text-white mb-3">Mobile App Development</h3>
                    <p class="text-gray-400 text-sm leading-relaxed mb-4">
                        Cross-platform mobile apps for Android and iOS using Flutter, integrated with Supabase or Firebase backends for real-time data sync, authentication, and push alerts.
                    </p>
                    <ul class="text-xs text-gray-400 space-y-2 border-t border-gray-800 pt-4">
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-cyan-400"></i> Flutter Cross-Platform</li>
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-cyan-400"></i> Supabase / Firebase Integration</li>
                    </ul>
                </div>

                <!-- Service 4 -->
                <div class="glass-card rounded-2xl p-8 transition-all duration-300 hover:-translate-y-2 relative group">
                    <div class="w-14 h-14 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
                        <i class="fa-solid fa-file-excel"></i>
                    </div>
                    <h3 class="text-xl font-bold text-white mb-3">Data Automation & Scraping</h3>
                    <p class="text-gray-400 text-sm leading-relaxed mb-4">
                        Streamlining manual tasks with Excel Power Query, automated PDF parsing, web scraping tools, and custom Python scripts that turn raw data into clean reports.
                    </p>
                    <ul class="text-xs text-gray-400 space-y-2 border-t border-gray-800 pt-4">
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-indigo-400"></i> Web Scraping & OCR Processing</li>
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-indigo-400"></i> Automated Excel Reporting</li>
                    </ul>
                </div>

                <!-- Service 5 -->
                <div class="glass-card rounded-2xl p-8 transition-all duration-300 hover:-translate-y-2 relative group">
                    <div class="w-14 h-14 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
                        <i class="fa-brands fa-figma"></i>
                    </div>
                    <h3 class="text-xl font-bold text-white mb-3">UI/UX Interface Design</h3>
                    <p class="text-gray-400 text-sm leading-relaxed mb-4">
                        User-centric interface wireframing, high-fidelity Figma prototypes, modern color palettes, and intuitive user experiences for web and mobile platforms.
                    </p>
                    <ul class="text-xs text-gray-400 space-y-2 border-t border-gray-800 pt-4">
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-cyan-400"></i> High-Fidelity Figma Prototypes</li>
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-cyan-400"></i> Modern Dark/Light Themes</li>
                    </ul>
                </div>

                <!-- Service 6 -->
                <div class="glass-card rounded-2xl p-8 transition-all duration-300 hover:-translate-y-2 relative group">
                    <div class="w-14 h-14 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform">
                        <i class="fa-solid fa-cubes"></i>
                    </div>
                    <h3 class="text-xl font-bold text-white mb-3">3D Architectural Visuals</h3>
                    <p class="text-gray-400 text-sm leading-relaxed mb-4">
                        Creation of clean 3D visual concepts, architectural representations, and spatial floor plans to showcase software solutions in physical domain contexts.
                    </p>
                    <ul class="text-xs text-gray-400 space-y-2 border-t border-gray-800 pt-4">
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-indigo-400"></i> Architectural & Layout Mockups</li>
                        <li class="flex items-center gap-2"><i class="fa-solid fa-angle-right text-indigo-400"></i> Spatial Visualization</li>
                    </ul>
                </div>

            </div>
        </div>
    </section>

    <!-- Projects Showcase Section -->
    <section id="projects" class="py-24 relative px-4 sm:px-6 lg:px-8 border-t border-gray-800/50">
        <div class="max-w-7xl mx-auto">
            <!-- Section Header -->
            <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
                <div class="space-y-3">
                    <div class="inline-flex items-center gap-2 text-cyan-400 font-semibold text-sm tracking-wider uppercase">
                        <i class="fa-solid fa-briefcase"></i> Portfolio Showcase
                    </div>
                    <h2 class="text-3xl sm:text-5xl font-extrabold text-white">
                        Featured Projects
                    </h2>
                </div>

                <!-- Filter Tabs -->
                <div class="flex flex-wrap gap-2 glass-card p-1.5 rounded-xl border border-gray-800">
                    <button class="filter-btn active px-4 py-2 rounded-lg text-xs font-semibold text-white bg-cyan-600 transition-all" data-filter="all">All</button>
                    <button class="filter-btn px-4 py-2 rounded-lg text-xs font-semibold text-gray-400 hover:text-white transition-all" data-filter="desktop">Desktop ERP</button>
                    <button class="filter-btn px-4 py-2 rounded-lg text-xs font-semibold text-gray-400 hover:text-white transition-all" data-filter="web">Web Portals</button>
                    <button class="filter-btn px-4 py-2 rounded-lg text-xs font-semibold text-gray-400 hover:text-white transition-all" data-filter="mobile">Mobile Apps</button>
                    <button class="filter-btn px-4 py-2 rounded-lg text-xs font-semibold text-gray-400 hover:text-white transition-all" data-filter="automation">Automation</button>
                </div>
            </div>

            <!-- Projects Grid -->
            <div id="projects-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

                <!-- Project 1 -->
                <div class="project-card glass-card rounded-2xl overflow-hidden border border-gray-800 flex flex-col" data-category="desktop">
                    <div class="h-48 bg-gradient-to-br from-cyan-900/40 to-indigo-900/40 p-6 flex flex-col justify-between relative overflow-hidden">
                        <div class="flex justify-between items-center z-10">
                            <span class="px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-mono">Python / Tkinter</span>
                            <i class="fa-solid fa-desktop text-2xl text-cyan-400"></i>
                        </div>
                        <div class="z-10">
                            <h4 class="text-xs text-cyan-400 font-mono">ERP & INVENTORY</h4>
                            <h3 class="text-xl font-bold text-white">Custom Inventory ERP System</h3>
                        </div>
                        <div class="absolute inset-0 bg-cyan-500/5 blur-2xl"></div>
                    </div>
                    <div class="p-6 flex-1 flex flex-col justify-between space-y-4">
                        <p class="text-sm text-gray-400 leading-relaxed">
                            Desktop software featuring offline SQLite synchronization, multi-user role management, barcode reader integration, and receipt printing.
                        </p>
                        <div class="flex items-center justify-between pt-4 border-t border-gray-800 text-xs">
                            <span class="text-gray-500">Tech: Python, SQLite, PySerial</span>
                            <a href="#contact" class="text-cyan-400 hover:underline flex items-center gap-1 font-semibold">
                                Details <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Project 2 -->
                <div class="project-card glass-card rounded-2xl overflow-hidden border border-gray-800 flex flex-col" data-category="web">
                    <div class="h-48 bg-gradient-to-br from-indigo-900/40 to-purple-900/40 p-6 flex flex-col justify-between relative overflow-hidden">
                        <div class="flex justify-between items-center z-10">
                            <span class="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-mono">FastAPI / Web</span>
                            <i class="fa-solid fa-bolt text-2xl text-indigo-400"></i>
                        </div>
                        <div class="z-10">
                            <h4 class="text-xs text-indigo-400 font-mono">REST API & PORTAL</h4>
                            <h3 class="text-xl font-bold text-white">Client Management Portal</h3>
                        </div>
                        <div class="absolute inset-0 bg-indigo-500/5 blur-2xl"></div>
                    </div>
                    <div class="p-6 flex-1 flex flex-col justify-between space-y-4">
                        <p class="text-sm text-gray-400 leading-relaxed">
                            A lightweight, rapid REST backend powered by FastAPI and PostgreSQL with interactive dashboard charts for real-time performance analytics.
                        </p>
                        <div class="flex items-center justify-between pt-4 border-t border-gray-800 text-xs">
                            <span class="text-gray-500">Tech: FastAPI, Tailwind, Chart.js</span>
                            <a href="#contact" class="text-cyan-400 hover:underline flex items-center gap-1 font-semibold">
                                Details <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Project 3 -->
                <div class="project-card glass-card rounded-2xl overflow-hidden border border-gray-800 flex flex-col" data-category="mobile">
                    <div class="h-48 bg-gradient-to-br from-blue-900/40 to-cyan-900/40 p-6 flex flex-col justify-between relative overflow-hidden">
                        <div class="flex justify-between items-center z-10">
                            <span class="px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-mono">Flutter / Supabase</span>
                            <i class="fa-solid fa-mobile-screen text-2xl text-cyan-400"></i>
                        </div>
                        <div class="z-10">
                            <h4 class="text-xs text-cyan-400 font-mono">CROSS-PLATFORM MOBILE</h4>
                            <h3 class="text-xl font-bold text-white">Field Service Mobile Utility</h3>
                        </div>
                        <div class="absolute inset-0 bg-cyan-500/5 blur-2xl"></div>
                    </div>
                    <div class="p-6 flex-1 flex flex-col justify-between space-y-4">
                        <p class="text-sm text-gray-400 leading-relaxed">
                            Mobile task tracking application featuring offline-first capabilities, Supabase authentication, photo attachment uploading, and push notifications.
                        </p>
                        <div class="flex items-center justify-between pt-4 border-t border-gray-800 text-xs">
                            <span class="text-gray-500">Tech: Flutter, Supabase</span>
                            <a href="#contact" class="text-cyan-400 hover:underline flex items-center gap-1 font-semibold">
                                Details <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Project 4 -->
                <div class="project-card glass-card rounded-2xl overflow-hidden border border-gray-800 flex flex-col" data-category="automation">
                    <div class="h-48 bg-gradient-to-br from-emerald-900/40 to-teal-900/40 p-6 flex flex-col justify-between relative overflow-hidden">
                        <div class="flex justify-between items-center z-10">
                            <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-mono">Automation</span>
                            <i class="fa-file-excel text-2xl text-emerald-400"></i>
                        </div>
                        <div class="z-10">
                            <h4 class="text-xs text-emerald-400 font-mono">DATA AUTOMATION</h4>
                            <h3 class="text-xl font-bold text-white">Automated PDF & Excel Parser</h3>
                        </div>
                        <div class="absolute inset-0 bg-emerald-500/5 blur-2xl"></div>
                    </div>
                    <div class="p-6 flex-1 flex flex-col justify-between space-y-4">
                        <p class="text-sm text-gray-400 leading-relaxed">
                            Python pipeline designed to automatically parse multi-page invoice PDFs, clean tabular data with Power Query, and export structured Excel reports.
                        </p>
                        <div class="flex items-center justify-between pt-4 border-t border-gray-800 text-xs">
                            <span class="text-gray-500">Tech: Python, Pandas, Power Query</span>
                            <a href="#contact" class="text-cyan-400 hover:underline flex items-center gap-1 font-semibold">
                                Details <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Project 5 -->
                <div class="project-card glass-card rounded-2xl overflow-hidden border border-gray-800 flex flex-col" data-category="desktop">
                    <div class="h-48 bg-gradient-to-br from-amber-900/40 to-orange-900/40 p-6 flex flex-col justify-between relative overflow-hidden">
                        <div class="flex justify-between items-center z-10">
                            <span class="px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 text-xs font-mono">Desktop / Hardware</span>
                            <i class="fa-solid fa-microchip text-2xl text-amber-400"></i>
                        </div>
                        <div class="z-10">
                            <h4 class="text-xs text-amber-400 font-mono">HARDWARE INTEGRATION</h4>
                            <h3 class="text-xl font-bold text-white">Serial Port Device Logger</h3>
                        </div>
                        <div class="absolute inset-0 bg-amber-500/5 blur-2xl"></div>
                    </div>
                    <div class="p-6 flex-1 flex flex-col justify-between space-y-4">
                        <p class="text-sm text-gray-400 leading-relaxed">
                            A PySerial desktop utility capturing live data feeds from hardware sensors and microcontrollers with real-time SQLite database logging.
                        </p>
                        <div class="flex items-center justify-between pt-4 border-t border-gray-800 text-xs">
                            <span class="text-gray-500">Tech: Python, PySerial, SQLite</span>
                            <a href="#contact" class="text-cyan-400 hover:underline flex items-center gap-1 font-semibold">
                                Details <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Project 6 -->
                <div class="project-card glass-card rounded-2xl overflow-hidden border border-gray-800 flex flex-col" data-category="web">
                    <div class="h-48 bg-gradient-to-br from-pink-900/40 to-rose-900/40 p-6 flex flex-col justify-between relative overflow-hidden">
                        <div class="flex justify-between items-center z-10">
                            <span class="px-3 py-1 rounded-full bg-pink-500/20 text-pink-300 text-xs font-mono">UI/UX Prototype</span>
                            <i class="fa-brands fa-figma text-2xl text-pink-400"></i>
                        </div>
                        <div class="z-10">
                            <h4 class="text-xs text-pink-400 font-mono">DESIGN SYSTEM</h4>
                            <h3 class="text-xl font-bold text-white">Modern SaaS UI Kit & Design</h3>
                        </div>
                        <div class="absolute inset-0 bg-pink-500/5 blur-2xl"></div>
                    </div>
                    <div class="p-6 flex-1 flex flex-col justify-between space-y-4">
                        <p class="text-sm text-gray-400 leading-relaxed">
                            Full Figma design system featuring comprehensive component libraries, dark/light themes, dynamic wireframes, and interactive prototype flows.
                        </p>
                        <div class="flex items-center justify-between pt-4 border-t border-gray-800 text-xs">
                            <span class="text-gray-500">Tech: Figma, Visual Architecture</span>
                            <a href="#contact" class="text-cyan-400 hover:underline flex items-center gap-1 font-semibold">
                                Details <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
                            </a>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <!-- GitHub Pages Deployment Guide Section -->
    <section id="github-guide" class="py-20 relative px-4 sm:px-6 lg:px-8 bg-gray-950/60 border-t border-gray-800/50">
        <div class="max-w-5xl mx-auto glass-card rounded-3xl p-8 sm:p-12 border border-cyan-500/20">
            <div class="flex items-center gap-3 text-cyan-400 font-semibold text-sm uppercase tracking-wider mb-2">
                <i class="fa-brands fa-github text-xl"></i> Deployment Guide
            </div>
            <h2 class="text-2xl sm:text-4xl font-extrabold text-white mb-4">
                How to Upload & Publish This Page on GitHub Pages
            </h2>
            <p class="text-gray-300 text-sm sm:text-base leading-relaxed mb-8">
                Follow these simple steps to host this single-page portfolio for free on <strong class="text-white">GitHub Pages</strong>:
            </p>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                <div class="glass-card p-5 rounded-xl border border-gray-800 space-y-2">
                    <div class="flex items-center gap-2 text-cyan-400 font-bold">
                        <span class="w-6 h-6 rounded-full bg-cyan-500/20 flex items-center justify-center text-xs">1</span>
                        Save File
                    </div>
                    <p class="text-gray-400">Save this complete code as <code class="text-cyan-300 bg-gray-900 px-2 py-0.5 rounded">index.html</code> on your computer.</p>
                </div>

                <div class="glass-card p-5 rounded-xl border border-gray-800 space-y-2">
                    <div class="flex items-center gap-2 text-cyan-400 font-bold">
                        <span class="w-6 h-6 rounded-full bg-cyan-500/20 flex items-center justify-center text-xs">2</span>
                        Create Repository
                    </div>
                    <p class="text-gray-400">Log into GitHub, click <strong>New Repository</strong>, name it (e.g., <code class="text-cyan-300 bg-gray-900 px-2 py-0.5 rounded">portfolio</code>), and keep it Public.</p>
                </div>

                <div class="glass-card p-5 rounded-xl border border-gray-800 space-y-2">
                    <div class="flex items-center gap-2 text-cyan-400 font-bold">
                        <span class="w-6 h-6 rounded-full bg-cyan-500/20 flex items-center justify-center text-xs">3</span>
                        Upload index.html
                    </div>
                    <p class="text-gray-400">Click <strong>"uploading an existing file"</strong>, drag and drop <code class="text-cyan-300 bg-gray-900 px-2 py-0.5 rounded">index.html</code>, and click <strong>Commit Changes</strong>.</p>
                </div>

                <div class="glass-card p-5 rounded-xl border border-gray-800 space-y-2">
                    <div class="flex items-center gap-2 text-cyan-400 font-bold">
                        <span class="w-6 h-6 rounded-full bg-cyan-500/20 flex items-center justify-center text-xs">4</span>
                        Enable GitHub Pages
                    </div>
                    <p class="text-gray-400">Go to <strong>Settings</strong> &gt; <strong>Pages</strong>. Under <em>Branch</em>, select <code class="text-cyan-300 bg-gray-900 px-2 py-0.5 rounded">main</code> (or master) and click <strong>Save</strong>. Your website will be live in 1-2 minutes!</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-24 relative px-4 sm:px-6 lg:px-8 border-t border-gray-800/50">
        <div class="max-w-7xl mx-auto">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
                
                <!-- Contact Information -->
                <div class="lg:col-span-5 space-y-6">
                    <div class="inline-flex items-center gap-2 text-cyan-400 font-semibold text-sm tracking-wider uppercase">
                        <i class="fa-regular fa-envelope"></i> Let's Connect
                    </div>
                    <h2 class="text-3xl sm:text-5xl font-extrabold text-white">
                        Have a Project in Mind?
                    </h2>
                    <p class="text-gray-300 leading-relaxed">
                        Whether you need a custom desktop ERP software, a fast web application, a cross-platform mobile app, or automation scripts, <strong class="text-white">Muzaffar Developers</strong> is ready to build it.
                    </p>

                    <div class="space-y-4 pt-4">
                        <div class="flex items-center gap-4 p-4 glass-card rounded-xl border border-gray-800">
                            <div class="w-12 h-12 rounded-lg bg-cyan-500/10 text-cyan-400 flex items-center justify-center text-xl">
                                <i class="fa-solid fa-envelope"></i>
                            </div>
                            <div>
                                <p class="text-xs text-gray-400">Email Address</p>
                                <a href="mailto:contact@muzaffardevelopers.com" class="text-sm font-semibold text-white hover:text-cyan-400 transition-colors">contact@muzaffardevelopers.com</a>
                            </div>
                        </div>

                        <div class="flex items-center gap-4 p-4 glass-card rounded-xl border border-gray-800">
                            <div class="w-12 h-12 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center text-xl">
                                <i class="fa-brands fa-github"></i>
                            </div>
                            <div>
                                <p class="text-xs text-gray-400">GitHub Profile</p>
                                <a href="https://github.com" target="_blank" class="text-sm font-semibold text-white hover:text-indigo-400 transition-colors">github.com/muzaffardev</a>
                            </div>
                        </div>

                        <div class="flex items-center gap-4 p-4 glass-card rounded-xl border border-gray-800">
                            <div class="w-12 h-12 rounded-lg bg-cyan-500/10 text-cyan-400 flex items-center justify-center text-xl">
                                <i class="fa-brands fa-linkedin-in"></i>
                            </div>
                            <div>
                                <p class="text-xs text-gray-400">LinkedIn</p>
                                <a href="https://linkedin.com" target="_blank" class="text-sm font-semibold text-white hover:text-cyan-400 transition-colors">linkedin.com/company/muzaffardevelopers</a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Contact Form -->
                <div class="lg:col-span-7">
                    <div class="glass-card p-8 rounded-3xl border border-gray-800 relative">
                        <form id="contact-form" class="space-y-6">
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                                <div>
                                    <label class="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Your Name</label>
                                    <input type="text" required placeholder="John Doe" class="w-full px-4 py-3 rounded-xl bg-gray-900/80 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition-colors text-sm">
                                </div>
                                <div>
                                    <label class="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Email Address</label>
                                    <input type="email" required placeholder="john@example.com" class="w-full px-4 py-3 rounded-xl bg-gray-900/80 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition-colors text-sm">
                                </div>
                            </div>

                            <div>
                                <label class="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Project Service Needed</label>
                                <select class="w-full px-4 py-3 rounded-xl bg-gray-900/80 border border-gray-700 text-white focus:outline-none focus:border-cyan-500 transition-colors text-sm">
                                    <option>Custom Desktop Software (Python / SQLite)</option>
                                    <option>Web Application (FastAPI / Flask)</option>
                                    <option>Mobile App (Flutter / Supabase)</option>
                                    <option>Data Automation & Scraping</option>
                                    <option>UI/UX & Architectural Visuals</option>
                                </select>
                            </div>

                            <div>
                                <label class="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Project Details</label>
                                <textarea rows="4" required placeholder="Briefly describe your requirements..." class="w-full px-4 py-3 rounded-xl bg-gray-900/80 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition-colors text-sm resize-none"></textarea>
                            </div>

                            <button type="submit" class="w-full py-4 rounded-xl bg-gradient-btn text-white font-semibold shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40 hover:scale-[1.01] active:scale-[0.99] transition-all flex items-center justify-center gap-2">
                                <i class="fa-regular fa-paper-plane"></i> Send Message
                            </button>
                        </form>

                        <!-- Success Alert Message Box -->
                        <div id="form-status" class="hidden mt-4 p-4 rounded-xl bg-green-500/20 border border-green-500/40 text-green-300 text-sm flex items-center gap-3">
                            <i class="fa-solid fa-circle-check text-green-400 text-xl"></i>
                            <span>Thank you! Your message has been received. We will get back to you shortly.</span>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="py-8 border-t border-gray-800/80 bg-gray-950/80 text-gray-400 text-xs">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-2">
                <span class="font-bold text-white">Muzaffar Developers</span> &copy; <span id="current-year"></span>. All rights reserved.
            </div>
            <div class="flex items-center space-x-6">
                <a href="#about" class="hover:text-cyan-400 transition-colors">About</a>
                <a href="#services" class="hover:text-cyan-400 transition-colors">Services</a>
                <a href="#projects" class="hover:text-cyan-400 transition-colors">Projects</a>
                <a href="#github-guide" class="hover:text-cyan-400 transition-colors">GitHub Pages Deploy</a>
            </div>
        </div>
    </footer>

    <script>
        // Set dynamic current year in footer
        document.getElementById('current-year').textContent = new Date().getFullYear();

        // Mobile Menu Toggle
        const mobileBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        const mobileLinks = document.querySelectorAll('.mobile-link');

        mobileBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });

        // Filterable Projects Gallery Logic
        const filterBtns = document.querySelectorAll('.filter-btn');
        const projectCards = document.querySelectorAll('.project-card');

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active class from all buttons
                filterBtns.forEach(b => {
                    b.classList.remove('active', 'bg-cyan-600', 'text-white');
                    b.classList.add('text-gray-400');
                });

                // Add active class to clicked button
                btn.classList.add('active', 'bg-cyan-600', 'text-white');
                btn.classList.remove('text-gray-400');

                const filterValue = btn.getAttribute('data-filter');

                projectCards.forEach(card => {
                    if (filterValue === 'all' || card.getAttribute('data-category') === filterValue) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });

        // Interactive Form Handler
        const contactForm = document.getElementById('contact-form');
        const formStatus = document.getElementById('form-status');

        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Show status feedback box
            formStatus.classList.remove('hidden');
            contactForm.reset();

            // Auto hide feedback after 5 seconds
            setTimeout(() => {
                formStatus.classList.add('hidden');
            }, 5000);
        });
    </script>
</body>
</html>
