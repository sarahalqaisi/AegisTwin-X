const $ = (id) => document.getElementById(id);

async function loadPromises() {
  const promises = await fetch('/api/promises').then(r => r.json());
  $('promises').innerHTML = promises.slice(0, 6).map(p => `
    <article class="promise">
      <strong>${p.title}</strong>
      <p>${p.description}</p>
      <code>${p.id} · ${p.severity.toUpperCase()}</code>
    </article>`).join('');
}

function renderGraph(graph) {
  const root = $('graph');
  root.innerHTML = '';
  const positions = {};
  const roleNodes = graph.nodes.filter(n => n.kind === 'role');
  const endpointNodes = graph.nodes.filter(n => n.kind === 'endpoint');
  const resourceNodes = graph.nodes.filter(n => n.kind === 'resource');
  const riskNodes = graph.nodes.filter(n => n.kind === 'risk');
  const place = (nodes, x, spread) => nodes.forEach((n, i) => positions[n.id] = {x, y: 55 + i * spread});
  place(roleNodes, 28, 85); place(endpointNodes, 245, 68); place(resourceNodes, 480, 78); place(riskNodes, 180, 115);
  graph.edges.forEach(e => {
    const a = positions[e.source], b = positions[e.target]; if (!a || !b) return;
    const length = Math.hypot(b.x-a.x, b.y-a.y), angle = Math.atan2(b.y-a.y,b.x-a.x)*180/Math.PI;
    const line = document.createElement('div'); line.className='edge';
    line.style.cssText=`left:${a.x+40}px;top:${a.y+16}px;width:${Math.max(15,length-65)}px;transform:rotate(${angle}deg);background:${e.protected===false?'#ff596d':'#46536a'}`;
    root.appendChild(line);
  });
  graph.nodes.forEach(n => { const p=positions[n.id]; const el=document.createElement('div'); el.className='node'; el.textContent=n.label; el.style.cssText=`left:${p.x}px;top:${p.y}px;--node:${n.color}`; root.appendChild(el); });
}

function renderFindings(findings) {
  const root = $('findings');
  if (!findings.length) { root.className='empty'; root.innerHTML='<span>✓</span><p>All security promises verified</p>'; return; }
  root.className='';
  root.innerHTML = findings.map(f => `
    <article class="finding">
      <div class="finding-head"><h3>${f.title}</h3><span class="severity">${f.severity.toUpperCase()} · VERIFIED</span></div>
      <p>${f.business_summary}</p>
      <div class="path">${f.attack_path.join(' → ')}</div>
      <div class="evidence"><span class="expected">Expected ${f.evidence.expected_status}</span><span>·</span><span class="observed">Observed ${f.evidence.observed_status}</span></div>
    </article>`).join('');
}

async function runAnalysis(variant) {
  document.body.classList.add('loading'); $('scanState').textContent='ANALYZING';
  try {
    const report = await fetch(`/api/analyses/demo?variant=${variant}`, {method:'POST'}).then(r => r.json());
    $('baseline').textContent=report.baseline_score; $('candidate').textContent=report.candidate_score;
    $('drift').textContent=report.security_dna_drift; $('verified').textContent=report.findings.length;
    $('decision').textContent=report.decision === 'BLOCK' ? 'Merge blocked' : 'Safe to merge';
    $('decision').style.color=report.decision === 'BLOCK' ? 'var(--red)' : 'var(--green)';
    $('scanState').textContent=report.decision; renderGraph(report.graph); renderFindings(report.findings);
  } finally { document.body.classList.remove('loading'); }
}

loadPromises();

