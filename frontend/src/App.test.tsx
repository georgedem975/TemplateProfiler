import { render, screen } from '@testing-library/react';
import { expect, it, describe } from 'vitest';
import App from './App';

describe('Prueba de humo del Frontend', () => {
  it('debe renderizar el título de la aplicación', () => {
    render(<App />);
    
    // Buscamos el texto que aparece en tu captura de pantalla
    const titleElement = screen.getByText(/TemplateProfiler/i);
    
    expect(titleElement).toBeInTheDocument();
  });
});