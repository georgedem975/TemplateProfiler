import Mustache from 'mustache';
import Handlebars from 'handlebars';
import _ from 'lodash';
import ejs from 'ejs';
import nunjucks from 'nunjucks';
import { Eta } from 'eta';
import type { EngineId, RenderResult } from '../types';

const eta = new Eta();

export const ENGINE_LABELS: Record<EngineId, string> = {
  mustache: 'Mustache',
  handlebars: 'Handlebars',
  lodash: 'Lodash (_.template)',
  ejs: 'EJS',
  nunjucks: 'Nunjucks',
  eta: 'Eta',
};

export function renderTemplate(engine: EngineId, template: string, dataJson: string): RenderResult {
  let data: unknown;
  try {
    data = JSON.parse(dataJson);
  } catch {
    throw new Error('Некорректный JSON в поле данных');
  }

  const start = performance.now();
  let output: string;

  switch (engine) {
    case 'mustache':
      output = Mustache.render(template, data as object);
      break;
    case 'handlebars': {
      const compiled = Handlebars.compile(template);
      output = compiled(data as object);
      break;
    }
    case 'lodash': {
      const compiled = _.template(template);
      output = compiled(data as object);
      break;
    }
    case 'ejs':
      output = ejs.render(template, data as object);
      break;
    case 'nunjucks':
      output = nunjucks.renderString(template, data as object);
      break;
    case 'eta':
      output = eta.renderString(template, data as object) ?? '';
      break;
  }

  const end = performance.now();
  return { output, render_time_ms: parseFloat((end - start).toFixed(3)) };
}
