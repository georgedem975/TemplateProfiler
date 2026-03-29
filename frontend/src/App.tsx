import { useState } from 'react';
import { TemplateSandbox } from './components/TemplateSandbox';
import { BenchmarkResults } from './components/BenchmarkResults';

type Tab = 'sandbox' | 'results';

export default function App() {
  const [tab, setTab] = useState<Tab>('sandbox');

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">TemplateProfiler</h1>
          <p className="text-sm text-gray-500 mt-1">Песочница для тестирования шаблонизаторов с замером времени рендеринга</p>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8">
        {/* Tabs */}
        <div className="flex gap-1 mb-6 bg-white rounded-lg p-1 shadow-sm w-fit">
          {(['sandbox', 'results'] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-5 py-2 rounded-md text-sm font-medium transition-colors ${
                tab === t
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {t === 'sandbox' ? 'Песочница' : 'Результаты'}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          {tab === 'sandbox' ? <TemplateSandbox /> : <BenchmarkResults />}
        </div>
      </main>
    </div>
  );
}
