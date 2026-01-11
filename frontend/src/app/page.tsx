import ChatWindow from '@/components/features/ChatWindow';

export default function Home() {
    return (
        <div className="min-h-screen bg-slate-50 flex flex-col">
            {/* Header */}
            <header className="bg-white border-b sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
                    <h1 className="text-2xl font-bold text-blue-600">AI Learning Coach</h1>
                    <nav className="flex gap-4">
                        <a href="#" className="text-slate-600 hover:text-blue-600">Dashboard</a>
                        <a href="#" className="text-slate-600 hover:text-blue-600">Curriculum</a>
                        <a href="#" className="text-slate-600 hover:text-blue-600">Profile</a>
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-1 max-w-7xl mx-auto w-full p-4 grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* Left Col: Curriculum / Stats Placeholder */}
                <div className="lg:col-span-1 space-y-6">
                    <div className="bg-white p-6 rounded-xl shadow-sm border">
                        <h2 className="text-lg font-semibold mb-4">Your Progress</h2>
                        <div className="space-y-4">
                            <div>
                                <div className="flex justify-between text-sm mb-1">
                                    <span>Python Mastery</span>
                                    <span className="font-medium">45%</span>
                                </div>
                                <div className="w-full bg-slate-100 rounded-full h-2">
                                    <div className="bg-green-500 h-2 rounded-full" style={{ width: '45%' }} />
                                </div>
                            </div>
                            <div className="p-4 bg-blue-50 rounded-lg text-sm text-blue-800">
                                <strong>Next Up:</strong> Advanced Pandas Functions
                            </div>
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-xl shadow-sm border">
                        <h2 className="text-lg font-semibold mb-4">Active Modules</h2>
                        <ul className="space-y-3">
                            <li className="flex items-center gap-2 text-sm">
                                <span className="w-2 h-2 rounded-full bg-green-500" />
                                Intro to Data Science
                            </li>
                            <li className="flex items-center gap-2 text-sm text-slate-500">
                                <span className="w-2 h-2 rounded-full bg-slate-300" />
                                Machine Learning Basics
                            </li>
                        </ul>
                    </div>
                </div>

                {/* Right Col: Chat Interface */}
                <div className="lg:col-span-2 flex justify-center">
                    <ChatWindow />
                </div>

            </main>
        </div>
    );
}
