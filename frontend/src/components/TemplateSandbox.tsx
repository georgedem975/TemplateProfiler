import { useState } from 'react';
import { renderTemplate, ENGINE_LABELS } from '../engines';
import { saveBenchmark } from '../api/benchmarks';
import type { EngineId, RenderResult } from '../types';

const DEFAULT_DATA = JSON.stringify({ name: 'Alice', count: 5, admin: true }, null, 2);

const ENGINE_EXAMPLES: Record<EngineId, string> = {
  mustache:   'Привет, {{name}}! У вас {{count}} сообщений.',
  handlebars: 'Привет, {{name}}! У вас {{count}} сообщений.',
  lodash:     'Привет, <%= name %>! У вас <%= count %> сообщений.',
  ejs:        'Привет, <%= name %>! У вас <%= count %> сообщений.',
  nunjucks:   'Привет, {{ name }}! У вас {{ count }} сообщений.',
  eta:        'Привет, <%= it.name %>! У вас <%= it.count %> сообщений.',
};

export function TemplateSandbox() {
  const [engine, setEngine] = useState<EngineId>('mustache');
  const [template, setTemplate] = useState(ENGINE_EXAMPLES.mustache);
  const [dataJson, setDataJson] = useState(DEFAULT_DATA);
  const [result, setResult] = useState<RenderResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'ok' | 'error'>('idle');

  function handleEngineChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const newEngine = e.target.value as EngineId;
    setEngine(newEngine);
    setTemplate(ENGINE_EXAMPLES[newEngine]);
    setResult(null);
    setError(null);
    setSaveStatus('idle');
  }

  function handleRender() {
    setError(null);
    setSaveStatus('idle');
    try {
      const r = renderTemplate(engine, template, dataJson);
      setResult(r);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка рендера');
      setResult(null);
    }
  }

  async function handleSave() {
    if (!result) return;
    setSaving(true);
    setSaveStatus('idle');
    try {
      await saveBenchmark({
        template_engine: engine,
        render_time_ms: result.render_time_ms,
        payload: dataJson,
      });
      setSaveStatus('ok');
    } catch {
      setSaveStatus('error');
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Engine selector */}
      <div className="flex items-center gap-3">
        <label className="font-medium text-gray-700">Шаблонизатор:</label>
        <select
          value={engine}
          onChange={handleEngineChange}
          className="border border-gray-300 rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          {(Object.keys(ENGINE_LABELS) as EngineId[]).map((id) => (
            <option key={id} value={id}>{ENGINE_LABELS[id]}</option>
          ))}
        </select>
      </div>

      {/* Editors */}
      <div className="grid grid-cols-2 gap-4">
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-600">Шаблон</label>
          <textarea
            value={template}
            onChange={(e) => setTemplate(e.target.value)}
            rows={8}
            className="font-mono text-sm border border-gray-300 rounded-md p-3 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Введите шаблон..."
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-gray-600">Данные (JSON)</label>
          <textarea
            value={dataJson}
            onChange={(e) => setDataJson(e.target.value)}
            rows={8}
            className="font-mono text-sm border border-gray-300 rounded-md p-3 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder='{"key": "value"}'
          />
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3">
        <button
          onClick={handleRender}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md text-sm font-medium hover:bg-indigo-700 transition-colors"
        >
          Рендер и замер
        </button>
        <button
          onClick={handleSave}
          disabled={!result || saving}
          className="px-4 py-2 bg-emerald-600 text-white rounded-md text-sm font-medium hover:bg-emerald-700 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {saving ? 'Сохранение...' : 'Сохранить в БД'}
        </button>
        {saveStatus === 'ok' && <span className="text-emerald-600 text-sm">Сохранено успешно</span>}
        {saveStatus === 'error' && <span className="text-red-500 text-sm">Ошибка сохранения (бэкенд недоступен?)</span>}
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-md px-4 py-3 text-sm">
          {error}
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-600">Время рендера:</span>
            <span className="text-sm font-mono font-bold text-indigo-700">{result.render_time_ms.toFixed(3)} ms</span>
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-600">Результат</label>
            <pre className="bg-gray-50 border border-gray-200 rounded-md p-4 text-sm font-mono whitespace-pre-wrap">
              {result.output}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
