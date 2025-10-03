window.setupAutoRefresh = function(apiUrl){
  const statusEl = document.getElementById("status");
  const listEl = document.getElementById("list");

  async function load(){
    try{
      const r = await fetch(apiUrl, { headers: { "Accept": "application/json" } });
      if(!r.ok) throw new Error("HTTP " + r.status);
      const j = await r.json();
      const count = j.count ?? (j.data ? j.data.length : 0);
      const when = (new Date()).toLocaleTimeString("pt-PT");
  statusEl.textContent = `Atualizado às ${when} • ${count} espaços ocupados`;
      render(j.data || []);
    }catch(e){
      console.error(e);
      statusEl.textContent = "Falha ao carregar dados";
    }
  }

  function esc(x){ return (x ?? "").toString().replace(/[&<>"']/g,s=>({ "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;" }[s])); }

  function card(it){
    return `
      <div class="row">
        <div style="width:100%">
          <div style="font-weight:800; letter-spacing:.3px; margin-bottom:6px; color:#ff4d4f;">
            ESPAÇO OCUPADO - ${esc(it.spaceName)}
          </div>
          <div class="muted" style="white-space:pre-line; line-height:1.6;">
Instituição : ${esc(it.instPretty)}
Campus : ${esc(it.campusPretty)}
Bloco : ${esc(it.buildingPretty)}
Área : ${esc(it.areaPretty)}
Espaço : ${esc(it.spaceName)}

Detalhes: ${esc(it.details || "-")}

Fim da Ocupação do Espaço : ${esc(it.endHuman)}
          </div>
        </div>
      </div>`;
  }

  function render(items){
    if(!listEl) return;
    listEl.innerHTML = "";
    if(!items.length){
  listEl.innerHTML = `<p class="muted">Sem espaços ocupados neste instante.</p>`;
      return;
    }
    for(const it of items){
      const div = document.createElement("div");
      div.innerHTML = card(it);
      listEl.appendChild(div.firstElementChild);
    }
  }

  load();
  const iv = setInterval(load, 30000);
  window.__manualRefresh = load;
  return ()=>clearInterval(iv);
};
