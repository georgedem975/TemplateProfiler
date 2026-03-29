export type EngineId = 'mustache' | 'handlebars' | 'lodash' | 'ejs' | 'nunjucks' | 'eta';

export interface BenchmarkResult {
  id?: number;
  template_engine: EngineId;
  render_time_ms: number;
  payload: string;
  created_at?: string;
}

export interface RenderResult {
  output: string;
  render_time_ms: number;
}
