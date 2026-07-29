const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
async function api(path, options) { const r=await fetch(path,options); if(!r.ok) throw new Error((await r.json()).detail||r.statusText); return r.json(); }
async function refresh() {
  const data=await Promise.all([api("/summary"),api("/entities"),api("/relationships")]), s=data[0], e=data[1], r=data[2];
  $("#metrics").innerHTML=[["Documents",s.documents],["Evidence chunks",s.chunks],["Graph entities",s.entities],["Relationships",s.relationships]]
    .map(x=>'<div class="metric"><small>'+x[0]+'</small><strong>'+x[1]+'</strong></div>').join("");
  $("#entities").innerHTML=e.entities.map(x=>'<span class="chip">'+esc(x.name)+' · '+esc(x.entity_type)+'</span>').join("");
  $("#relationships").innerHTML=r.relationships.slice(0,20).map(x=>'<div class="item edge"><b>'+esc(x.source_entity)+'</b><i>—'+esc(x.relationship_type)+'→</i><b>'+esc(x.target_entity)+'</b></div>').join("");
}
$("#ingest").onclick=async()=>{await api("/documents/ingest",{method:"POST"});await refresh();};
$("#ask").onclick=async()=>{try{
  const q=$("#question").value, opts={method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:q})};
  const data=await Promise.all([api("/ask",opts),api("/retrieve",opts)]), a=data[0], r=data[1];
  $("#answer").classList.remove("empty");
  $("#answer").innerHTML='<b>'+esc(a.confidence.toUpperCase())+' CONFIDENCE</b><p>'+esc(a.answer)+'</p><small>'+esc(a.uncertainty_note)+'</small>';
  $("#graph").innerHTML=a.graph_evidence.length?a.graph_evidence.map(x=>'<div class="item edge"><b>'+esc(x.source)+'</b><i>—'+esc(x.relationship)+'→</i><b>'+esc(x.target)+'</b><span class="citation">'+esc(x.citation)+'</span></div>').join(""):'<span class="empty">No graph edge was needed.</span>';
  $("#chunks").innerHTML=r.top_chunks.map(x=>'<div class="item"><b>'+esc(x.document_name)+' / '+esc(x.section_title)+'</b><p>'+esc(x.chunk_text.slice(0,260))+'</p><span class="citation">'+esc(x.chunk_id)+'</span></div>').join("");
}catch(e){$("#answer").textContent=e.message;}};
$("#evaluate").onclick=async()=>{const d=await api("/evaluate",{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"}), scores=d.evaluations[0].scores;
  $("#scores").innerHTML=Object.entries(scores).map(x=>'<div class="score"><span>'+esc(x[0].replaceAll("_"," "))+'</span><b>'+Math.round(x[1]*100)+'%</b></div>').join("")+'<div class="score"><span>Suite average</span><b>'+Math.round(d.average*100)+'%</b></div>';
};
(async()=>{try{await refresh();if(!$("#entities").children.length){await api("/documents/ingest",{method:"POST"});await refresh();}}catch(e){console.error(e);}})();
