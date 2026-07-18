// KIKSLAB app — all UI logic
// movies.js loads first via defer, providing window.SCRAPER_MOVIES + window.SCRAPER_LINKS

const TMDB_KEY = "029922d0ce729264a5fcd6f7403ec732";
const IMG = "https://image.tmdb.org/t/p/w500";
const BACKDROP = "https://image.tmdb.org/t/p/w1280";
const TG = "https://t.me/KiksLabMovies";
const LINKS = (window.SCRAPER_LINKS) || {};
function getLink(t){ return LINKS[t] || TG; }

const ROWS = [
  {key:"trending", title:"🔥 Trending Now"},{key:"new", title:"🆕 New Releases"},
  {key:"popular", title:"⭐ Most Popular"},{key:"top_rated", title:"🏆 Top Rated"},
  {key:"bollywood", title:"🇮🇳 Bollywood Hits"},{key:"south", title:"🌏 South Hindi Dubbed"},
  {key:"tollywood", title:"🔥 Tollywood"},{key:"hollywood", title:"🎬 Hollywood"},
  {key:"bangla", title:"🇧🇩 Bangla Dubbed"},{key:"action", title:"💥 Action"},
  {key:"comedy", title:"😂 Comedy"},{key:"crime", title:"🔫 Crime"},
  {key:"drama", title:"🎭 Drama"},{key:"horror", title:"👻 Horror"},
  {key:"romance", title:"💕 Romance"},{key:"scifi", title:"🚀 Sci-Fi"},
  {key:"thriller", title:"😱 Thriller"},{key:"fantasy", title:"🧙 Fantasy"},
  {key:"mystery", title:"🔍 Mystery"},{key:"adventure", title:"🗺️ Adventure"},
  {key:"animation", title:"🎨 Animation"},{key:"family", title:"👨‍👩‍👧 Family"},
  {key:"history", title:"📜 History"},{key:"war", title:"⚔️ War"},
  {key:"music", title:"🎵 Music"},{key:"anime", title:"🌸 Anime"},
  {key:"now_playing", title:"🎥 Now Playing"},{key:"upcoming", title:"📅 Upcoming"},
  {key:"western", title:"🤠 Western"},{key:"documentary", title:"📽️ Documentary"},
  {key:"tv_movie", title:"📺 TV Movie"},{key:"korean", title:"🇰🇷 Korean"},
  {key:"japanese", title:"🇯🇵 Japanese"},{key:"chinese", title:"🇨🇳 Chinese"},
  {key:"russian", title:"🇷🇺 Russian"},
];
const SM = (window.SCRAPER_MOVIES) || [];
let currentMovie = null;

document.addEventListener("DOMContentLoaded", () => {

// ===== SEARCH =====
const SI = document.getElementById("sinput");
const SD = document.getElementById("sdrop");
let sTimer = null;
SI.addEventListener("input", ()=>{
  clearTimeout(sTimer);
  const q = SI.value.trim().toLowerCase();
  if(!q){ SD.classList.remove("show"); SD.innerHTML=""; return; }
  sTimer = setTimeout(()=>{
    const hits = SM.filter(m=> (m.title||"").toLowerCase().includes(q)).slice(0,12);
    if(!hits.length){
      SD.innerHTML=`<div style="padding:18px;color:#888;text-align:center">Not found</div><a class="tg-opt" href="https://t.me/KiksLabMovies" target="_blank">📩 Search on Telegram</a>`;
      SD.classList.add("show"); return;
    }
    SD.innerHTML = hits.map(m=>`<div class="si" onclick="searchPick(${m.tmdb_id})">
      <img src="${m.poster||''}" alt="" onerror="this.style.display='none'">
      <div class="st"><b>${(m.title||'').replace(/'/g,'')}</b><small>${m.year||'—'} • ${(m._sec||'')}</small></div>
      <span class="sr">★ ${m.rating?m.rating.toFixed(1):'?'}</span>
    </div>`).join("") + `<a class="tg-opt" href="https://t.me/KiksLabMovies" target="_blank">📩 Not found? Search on Telegram</a>`;
    SD.classList.add("show");
  }, 250);
});
function searchPick(id){
  SD.classList.remove("show"); SI.value="";
  const m = SM.find(x=>x.tmdb_id===id);
  if(m) openModal(m);
}
document.addEventListener("click", e=>{ if(!e.target.closest(".search-wrap") && !e.target.closest("#sdrop")) SD.classList.remove("show"); });

// ===== BUILD UI =====
buildRows();
setHero();
setInterval(()=>{ hi++; setHero(); }, 6000);

// HERO
let heroList = SM.filter(m=>m._sec==="trending");
if(!heroList.length) heroList = SM.slice(0,20);
let hi = 0;
function setHero(){
  const m = heroList[hi % heroList.length];
  if(!m) return;
  const h = document.getElementById("hero");
  if(m.poster) h.style.backgroundImage = `url('${BACKDROP + m.poster.split('/w500')[1]}')`;
  document.getElementById("h-title").textContent = m.title;
  document.getElementById("h-rate").textContent = "★ " + (m.rating?m.rating.toFixed(1):'—');
  document.getElementById("h-year").textContent = m.year||'—';
  document.getElementById("h-overview").textContent = m.overview||"";
  document.getElementById("h-play").onclick = ()=>{ openPlayer(m); };
  document.getElementById("h-dl").href = getLink(m.title);
  document.getElementById("h-info").onclick = ()=>openModal(m);
}

// ROWS
function buildRows(){
  const rows = document.getElementById("rows");
  rows.innerHTML = "";
  ROWS.forEach(r=>{
    const list = SM.filter(m=>m._sec===r.key);
    if(!list.length) return;
    const sec = document.createElement("section");
    sec.className = "row";
    sec.innerHTML = `<h2 class="sec-title">${r.title}</h2>
      <div class="shelf">${list.map(tile).join("")}</div>`;
    rows.appendChild(sec);
  });
  // category strip
  const cs = document.getElementById("catstrip");
  cs.innerHTML = ROWS.map(r=>`<a href="#" data-key="${r.key}">${r.title}</a>`).join("");
  cs.querySelectorAll("a").forEach(a=>{
    a.addEventListener("click", e=>{ e.preventDefault(); jumpTo(a.dataset.key); });
  });
}
function jumpTo(key){
  const map = {}; ROWS.forEach((r,i)=>map[r.key]=i);
  const target = document.querySelectorAll(".row")[map[key]];
  if(target) target.scrollIntoView({behavior:"smooth"});
}
function tile(m){
  const rate = m.rating?m.rating.toFixed(1):'?';
  const ttl = (m.title||'').replace(/\"/g,'&quot;').replace(/'/g,"");
  return `<div class="tile" style="background-image:url('${m.poster}')">
    <span class="rate">★ ${rate}</span>
    <div class="tinfo"><b>${ttl}</b><small>${m.year||'—'} • HD</small></div>
    <div class="dl" onclick="event.stopPropagation();openAds();showToast('${ttl}')">⬇</div>
    <div class="tileclick" onclick="tileClick(event, ${m.tmdb_id})"></div>
  </div>`;
}
function tileClick(e, id){
  if(e.target.closest('.dl')) return;
  const m = SM.find(x=>x.tmdb_id===id) || {};
  if(window._clk!==id){ window._clk=id; openAds(); showToast((m.title||'')+" — ad loaded, click again"); setTimeout(()=>{if(window._clk===id)window._clk=null;},4000); }
  else { window._clk=null; openModal(m); }
}

// MODAL
function openModal(m){
  currentMovie = m;
  openAds();
  const bg = m.poster ? BACKDROP + m.poster.split('/w500')[1] : "";
  if(bg) document.getElementById("m-bg").style.backgroundImage = `url('${bg}')`;
  document.getElementById("m-title").textContent = m.title;
  document.getElementById("m-meta").textContent = "★ " + (m.rating?m.rating.toFixed(1):'—') + "  •  " + (m.year||'—');
  document.getElementById("m-overview").textContent = m.overview||"";
  const tl = document.getElementById("m-trailer");
  if(m.trailer){ tl.href=m.trailer; tl.style.display="inline-flex"; } else tl.style.display="none";
  document.getElementById("m-dl").href = getLink(m.title);
  document.getElementById("modal").classList.add("show");
}
function closeModal(){ document.getElementById("modal").classList.remove("show"); }

// PLAYER
const SERVERS = [
  {n:"Server 1", base:"https://vidsrc.to/embed/movie/"},
  {n:"Server 2", base:"https://vidlink.pro/movie/"},
  {n:"Server 3", base:"https://www.2embed.to/embed/movie/"},
  {n:"Server 4", base:"https://vidsrc.icu/embed/movie/"},
  {n:"Server 5", base:"https://moviesapi.to/movie/"},
  {n:"Server 6", base:"https://embed.smashy.stream/movie/"},
];
let _curM = null;
function openPlayer(m){
  openAds();
  _curM = m;
  if(!m.tmdb_id){ window.location.href = getLink(m.title); return; }
  const p = document.getElementById("player");
  p.innerHTML = `<div style="padding:16px"><div style="color:#fff;font-weight:700;margin-bottom:8px">🎬 ${m.title}</div>
    <div id="srv-list">` +
    SERVERS.map((s,i)=>`<button class="srvbtn" onclick="goServer(${i})" style="display:block;width:100%;margin:6px 0;padding:12px;background:#222;color:#fff;border:1px solid #444;border-radius:6px;cursor:pointer;font-size:15px">▶ ${s.n}</button>`).join("") +
    `</div><a href="${getLink(m.title)}" target="_blank" style="display:block;width:100%;margin:6px 0;padding:12px;background:#e50914;color:#fff;text-align:center;border-radius:6px;font-weight:700">⬇ Download HD</a></div>`;
  document.getElementById("playmodal").classList.add("show");
  autoTry(0);
}
function autoTry(i){
  if(i>=SERVERS.length) return;
  const m=_curM; if(!m) return;
  const w = window.open(SERVERS[i].base + m.tmdb_id, "_blank", "noopener");
  if(!w) return;
  setTimeout(()=>{
    const modalStill = document.getElementById("playmodal").classList.contains("show");
    if(modalStill && _curM===m) autoTry(i+1);
  }, 8000);
}
function goServer(i){ const m=_curM; if(m) window.location.href = SERVERS[i].base + m.tmdb_id; }
function closePlay(){ document.getElementById("playmodal").classList.remove("show"); document.getElementById("player").innerHTML=""; }

function showToast(n){
  const t=document.getElementById("toast");
  t.textContent="⬇ "+n+" — opening download...";
  t.classList.add("show");
  setTimeout(()=>t.classList.remove("show"),2200);
}

// NAV
document.querySelectorAll('nav a[data-f]').forEach(a=>{
  a.addEventListener('click', e=>{ e.preventDefault();
    const f=a.dataset.f; const list=SM.filter(m=>m._sec===f);
    if(list.length){ document.getElementById("rows").scrollIntoView({behavior:"smooth"}); }
  });
});

// HEADER BG
window.addEventListener('scroll', ()=>{
  document.getElementById("hdr").style.background = window.scrollY>60 ? "#000" : "linear-gradient(180deg,rgba(0,0,0,.9),transparent)";
});

}); // DOMContentLoaded
