export const join = (...parts: string[]) => parts.join('/');
export const dirname = (p: string) => p.split('/').slice(0, -1).join('/');
export const extname = (p: string) => { const i = p.lastIndexOf('.'); return i >= 0 ? p.slice(i) : ''; };
export const isAbsolute = (p: string) => p.startsWith('/');
export const relative = (_from: string, to: string) => to;
export default { join, dirname, extname, isAbsolute, relative };
