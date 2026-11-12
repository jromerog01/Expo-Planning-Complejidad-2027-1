// Genera mapas reales (Natural Earth 1:50m, world-atlas):
//   node generar-mapa.mjs ../../img/flights.svg            -> plan completo con escalas
//   node generar-mapa.mjs ../../img/flights-directo.svg directo -> solo el vuelo directo CDMX -> Tokio, tachado
import fs from 'node:fs';
import * as d3 from 'd3-geo';
import * as topojson from 'topojson-client';

const out = process.argv[2];
const directo = process.argv[3] === 'directo';
const load = r => { const w = JSON.parse(fs.readFileSync(new URL(`./node_modules/world-atlas/countries-${r}.json`, import.meta.url))); return topojson.feature(w, w.objects.countries).features; };
const countries = load('110m');      // mapa general
const detail = load('50m');          // recuadro ampliado de Europa
const W = 1448, H = 386;
const f = n => n.toFixed(1);

const city = {
  mex: { name: 'Ciudad de México', c: [-99.13, 19.43] },
  la:  { name: 'Los Ángeles',      c: [-118.24, 34.05] },
  mad: { name: 'Madrid',           c: [-3.70, 40.42] },
  par: { name: 'París',            c: [2.35, 48.86] },
  tyo: { name: 'Tokio',            c: [139.69, 35.68] },
};
const legs = [['mex','la','O_2'], ['la','mad','O_3'], ['mad','tyo','O_7']];

// Proyección principal: Natural Earth, ajustada a las rutas (misma en ambos mapas)
const routeGeo = { type: 'FeatureCollection', features: [
  ...legs.map(([a,b]) => ({ type:'Feature', geometry:{ type:'LineString', coordinates:[city[a].c, city[b].c] } })),
  { type:'Feature', geometry:{ type:'MultiPoint', coordinates:[[-150, 2], [158, 2], [-20, 70]] } },
]};
const proj = d3.geoNaturalEarth1().rotate([-12, 0]).fitExtent([[60, 40], [W - 60, H - 30]], routeGeo);
const path = d3.geoPath(proj).digits(1);
const P = c => proj(c);

const highlight = new Set(['484', '840', '724', '250', '392']);
let svg = [];
svg.push(`<svg class="ill" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${directo ? 'Mapa: no hay vuelo directo de Ciudad de México a Tokio' : 'Mapa: Ciudad de México, Los Ángeles, Madrid, París, Madrid, Tokio'}">`);
svg.push(`  <path d="${path(d3.geoGraticule10())}" fill="none" stroke="#ffffff" stroke-opacity=".35" stroke-width=".8"/>`);
for (const ft of countries) {
  const d = path(ft); if (!d) continue;
  const hi = highlight.has(ft.id);
  svg.push(`  <path d="${d}" fill="#ffffff" fill-opacity="${hi ? '.92' : '.5'}" stroke="#ffffff" stroke-opacity=".9" stroke-width="${hi ? 1.2 : .6}"/>`);
}

// Rutas largas (gran círculo), recortadas para que la flecha no tape el punto
function leg(a, b, t0, t1) {
  const it = d3.geoInterpolate(city[a].c, city[b].c);
  const pts = Array.from({ length: 41 }, (_, i) => i).map(i => it(t0 + (t1 - t0) * i / 40));
  return path({ type: 'LineString', coordinates: pts });
}
const badges = [];
for (const [a, b, op] of (directo ? [] : legs)) {
  svg.push(`  <path d="${leg(a, b, 0.03, 0.965)}" fill="none" stroke="#1f4a7d" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>`);
  badges.push([P(d3.geoInterpolate(city[a].c, city[b].c)(0.5)), op]);
}
// Ciudades
const dot = (k, r, fill) => { const [x, y] = P(city[k].c); return `  <circle cx="${f(x)}" cy="${f(y)}" r="${r}" fill="${fill}" stroke="#fff" stroke-width="3"/>`; };
if (directo) svg.push(dot('mex', 8, 'url(#g-ink)'), dot('tyo', 9, 'url(#g-blue)'));
else svg.push(dot('mex', 8, 'url(#g-ink)'), dot('la', 7, '#1f4a7d'), dot('mad', 7, '#1f4a7d'), dot('par', 6, '#1f4a7d'), dot('tyo', 9, 'url(#g-blue)'));

// Etiquetas de ciudad (tarjetas de vidrio)
function label(k, dx, dy, w, sub) {
  const [x, y] = P(city[k].c); const h = sub ? 58 : 38; const X = x + dx, Y = y + dy;
  let s = `  <rect class="glass" x="${f(X)}" y="${f(Y)}" width="${w}" height="${h}" rx="12"/>\n`;
  s += `  <text x="${f(X + 14)}" y="${f(Y + 25)}" font-size="16" font-weight="650">${city[k].name}</text>`;
  if (sub) s += `\n  <foreignObject x="${f(X + 14)}" y="${f(Y + 32)}" width="${w - 20}" height="22"><div xmlns="http://www.w3.org/1999/xhtml" class="fo t-accent" style="font-size:13px;font-weight:600;height:22px">${sub}</div></foreignObject>`;
  return s;
}
if (directo) {
  svg.push(label('mex', -76, 16, 176));
  svg.push(label('tyo', -50, 16, 110));
} else {
  svg.push(label('mex', -76, 16, 176, '+ visa EUA \\(O_1\\)'));
  svg.push(label('la', -150, -54, 128));
  svg.push(label('tyo', -60, 16, 150, 'meta \\(S^*\\)'));
}

// Vuelo directo imposible: una flecha de CDMX a Tokio con un tache en medio
if (directo) {
  const [x1, y1] = P(city.mex.c), [x2, y2] = P(city.tyo.c);
  const c = [(x1 + x2) / 2, Math.max(24, Math.min(y1, y2) - 190)];
  const q = t => [(1 - t) ** 2 * x1 + 2 * (1 - t) * t * c[0] + t * t * x2, (1 - t) ** 2 * y1 + 2 * (1 - t) * t * c[1] + t * t * y2];
  const pts = Array.from({ length: 41 }, (_, i) => q(0.03 + (0.965 - 0.03) * i / 40));
  svg.push(`  <path d="M${pts.map(([x, y]) => f(x) + ' ' + f(y)).join(' L')}" fill="none" stroke="#1f4a7d" stroke-width="3" stroke-linecap="round" marker-end="url(#arrow)"/>`);
  const [mx, my] = q(0.5);
  svg.push(`  <circle cx="${f(mx)}" cy="${f(my)}" r="24" fill="#b0413e" stroke="#fff" stroke-width="3"/>`);
  svg.push(`  <path d="M${f(mx - 9)} ${f(my - 9)} L${f(mx + 9)} ${f(my + 9)} M${f(mx + 9)} ${f(my - 9)} L${f(mx - 9)} ${f(my + 9)}" stroke="#fff" stroke-width="5" stroke-linecap="round"/>`);
}

// Insertos de operador
for (const [[x, y], op] of badges) {
  svg.push(`  <circle cx="${f(x)}" cy="${f(y)}" r="15" fill="#2f6fb5" stroke="#fff" stroke-width="2.5"/>`);
  svg.push(`  <foreignObject x="${f(x - 30)}" y="${f(y - 13)}" width="60" height="26"><div xmlns="http://www.w3.org/1999/xhtml" class="fo t-white" style="font-size:13px;font-weight:700;justify-content:center;height:26px">\\(${op}\\)</div></foreignObject>`);
}

// Recuadro ampliado: Madrid <-> París
if (!directo) {
const box = { x: 820, y: 196, w: 290, h: 172 };
const [mx, my] = P(city.mad.c), [px, py] = P(city.par.c);
svg.push(`  <path d="M${f(mx)} ${f(my)} L${box.x} ${box.y + 40}" stroke="#1f4a7d" stroke-width="1.5" stroke-dasharray="3 5" fill="none"/>`);
svg.push(`  <path d="M${f(px)} ${f(py)} L${box.x + 40} ${box.y}" stroke="#1f4a7d" stroke-width="1.5" stroke-dasharray="3 5" fill="none"/>`);
svg.push(`  <rect class="glass" x="${box.x}" y="${box.y}" width="${box.w}" height="${box.h}" rx="18"/>`);
const zoom = d3.geoMercator().fitExtent([[box.x + 12, box.y + 12], [box.x + box.w - 12, box.y + box.h - 12]],
  { type: 'MultiPoint', coordinates: [[-10, 35.5], [9, 52]] });
const zpath = d3.geoPath(zoom).digits(1);
svg.push(`  <clipPath id="clip-eu"><rect x="${box.x + 4}" y="${box.y + 4}" width="${box.w - 8}" height="${box.h - 8}" rx="15"/></clipPath>`);
svg.push(`  <g clip-path="url(#clip-eu)">`);
svg.push(`    <rect x="${box.x}" y="${box.y}" width="${box.w}" height="${box.h}" fill="#cfe2f6"/>`);
const inBox = ft => { const [[x0, y0], [x1, y1]] = d3.geoBounds(ft); return x1 > -12 && x0 < 12 && y1 > 34 && y0 < 54; };
for (const ft of detail.filter(inBox)) {
  const d = zpath(ft); if (!d) continue;
  const hi = ft.id === '724' || ft.id === '250';
  svg.push(`    <path d="${d}" fill="#ffffff" fill-opacity="${hi ? '1' : '.6'}" stroke="#9fb6cf" stroke-width=".8"/>`);
}
const [zmx, zmy] = zoom(city.mad.c), [zpx, zpy] = zoom(city.par.c);
// O4 (Madrid -> París) y O6 (París -> Madrid) como dos arcos
svg.push(`    <path d="M${f(zmx + 6)} ${f(zmy - 8)} Q ${f(zmx - 30)} ${f((zmy + zpy) / 2)} ${f(zpx - 8)} ${f(zpy + 5)}" fill="none" stroke="#1f4a7d" stroke-width="2.6" marker-end="url(#arrow)"/>`);
svg.push(`    <path d="M${f(zpx + 4)} ${f(zpy + 9)} Q ${f(zpx + 46)} ${f((zmy + zpy) / 2 + 10)} ${f(zmx + 10)} ${f(zmy - 2)}" fill="none" stroke="#1f4a7d" stroke-width="2.6" stroke-dasharray="2 6" stroke-linecap="round" marker-end="url(#arrow)"/>`);
svg.push(`    <circle cx="${f(zmx)}" cy="${f(zmy)}" r="7" fill="#1f4a7d" stroke="#fff" stroke-width="2.5"/>`);
svg.push(`    <circle cx="${f(zpx)}" cy="${f(zpy)}" r="7" fill="#1f4a7d" stroke="#fff" stroke-width="2.5"/>`);
svg.push(`  </g>`);
const zb = (x, y, op) => `  <circle cx="${f(x)}" cy="${f(y)}" r="13" fill="#2f6fb5" stroke="#fff" stroke-width="2"/>\n  <foreignObject x="${f(x - 30)}" y="${f(y - 12)}" width="60" height="24"><div xmlns="http://www.w3.org/1999/xhtml" class="fo t-white" style="font-size:12px;font-weight:700;justify-content:center;height:24px">\\(${op}\\)</div></foreignObject>`;
svg.push(zb(zmx - 28, (zmy + zpy) / 2, 'O_4'));
svg.push(zb(zpx + 34, (zmy + zpy) / 2 + 8, 'O_6'));
svg.push(`  <text x="${f(zmx + 12)}" y="${f(zmy + 22)}" font-size="14" font-weight="650">Madrid</text>`);
svg.push(`  <text x="${f(zpx + 12)}" y="${f(zpy - 6)}" font-size="14" font-weight="650">París</text>`);
svg.push(`  <foreignObject x="${f(zpx + 12)}" y="${f(zpy - 2)}" width="120" height="20"><div xmlns="http://www.w3.org/1999/xhtml" class="fo t-accent" style="font-size:12px;font-weight:600;height:20px">+ visa JP \\(O_5\\)</div></foreignObject>`);
}

svg.push(`  <text x="${W - 24}" y="${H - 14}" font-size="11" text-anchor="end" fill="#4c5a6b" fill-opacity=".8">Mapa: Natural Earth · ${directo ? 'esquema ilustrativo' : 'rutas de gran círculo'} · instancia ficticia</text>`);
svg.push('</svg>');
fs.writeFileSync(out, svg.join('\n') + '\n');
console.log('ok', (fs.statSync(out).size / 1024).toFixed(0) + ' KB');
