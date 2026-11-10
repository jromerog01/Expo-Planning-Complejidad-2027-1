// Exporta presentacion.html a presentacion.pdf (vectorial, igual al HTML).
// Uso: npm install && npx playwright install chromium && npm run pdf
import { chromium } from 'playwright';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const html = path.resolve(aqui, '../../presentacion.html');
const pdf = path.resolve(aqui, '../../presentacion.pdf');

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
await page.goto('file://' + html + '?print-pdf');
await page.waitForFunction(() => window.Reveal && Reveal.isReady());
await page.evaluate(() => document.fonts.ready);
await page.waitForFunction(() => window.MathJax?.startup?.promise);
await page.evaluate(() => MathJax.startup.promise);   // esperar a que se dibuje el LaTeX
await page.waitForTimeout(2000);
await page.emulateMedia({ media: 'print' });
await page.pdf({ path: pdf, width: '1600px', height: '900px', printBackground: true,
                 margin: { top: 0, right: 0, bottom: 0, left: 0 } });
await browser.close();
console.log('PDF generado:', pdf);
