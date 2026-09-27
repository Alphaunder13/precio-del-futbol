var teams=[
{id:0,n:'Inferno FC',i:'🔥',g:'A',pts:118,money:225,cups:0},
{id:1,n:'Titan FC',i:'⚔️',g:'A',pts:172,money:900,cups:1},
{id:2,n:'Atlántico',i:'🌊',g:'A',pts:146,money:375,cups:0},
{id:3,n:'Furia 7',i:'🐺',g:'A',pts:201,money:1800,cups:2},
{id:4,n:'Basalto CF',i:'⬛',g:'A',pts:82,money:0,cups:0},
{id:5,n:'Magma United',i:'🌋',g:'B',pts:96,money:0,cups:0},
{id:6,n:'Los Diablos',i:'😈',g:'B',pts:157,money:900,cups:1},
{id:7,n:'Caldera 10',i:'🦂',g:'B',pts:75,money:0,cups:0},
{id:8,n:'Roque City',i:'🪨',g:'B',pts:64,money:0,cups:0},
{id:9,n:'Lava Boys',i:'☄️',g:'B',pts:55,money:0,cups:0}
];
var matches={
A:[['Inferno FC','Basalto CF',2,1],['Titan FC','Furia 7',1,1],['Inferno FC','Furia 7',3,0],['Basalto CF','Titan FC',0,2],['Inferno FC','Atlántico',1,1],['Furia 7','Basalto CF',2,2],['Atlántico','Titan FC',0,1],['Inferno FC','Titan FC',2,3],['Atlántico','Basalto CF',2,0],['Atlántico','Furia 7',1,0]],
B:[['Magma United','Lava Boys',2,0],['Los Diablos','Caldera 10',2,2],['Magma United','Caldera 10',1,0],['Lava Boys','Los Diablos',1,3],['Magma United','Roque City',2,2],['Caldera 10','Lava Boys',1,0],['Roque City','Los Diablos',0,1],['Magma United','Los Diablos',1,2],['Roque City','Lava Boys',3,1],['Roque City','Caldera 10',2,0]]
};
var playoffs={eruption:[['Atlántico','Caldera 10',2,1],['Los Diablos','Titan FC',3,2]],semi:[['Inferno FC','Los Diablos',2,1],['Magma United','Atlántico',1,2]],third:[['Magma United','Los Diablos',null,null]],final:[['Inferno FC','Atlántico',null,null]]};
var S={tab:'home',group:'A',rank:'rank',admin:false,checked:86};
try{var saved=JSON.parse(localStorage.getItem('volcanoCupMobile'));if(saved)Object.assign(S,saved)}catch(e){}
function save(){try{localStorage.setItem('volcanoCupMobile',JSON.stringify(S))}catch(e){}}
function euro(v){return v.toLocaleString('es-ES')+' €'} function pool(){return S.checked*15} function field(){return S.checked*2}
function icon(n){var t=teams.find(function(x){return x.n===n});return t?t.i:'•'}
function top(){return '<div class="top"><div class="brand"><div class="logo">🌋</div><div><b>VOLCANO CUP</b><small>CASH FOOTBALL CIRCUIT</small></div></div><button class="gear" onclick="toggleAdmin()">'+(S.admin?'✕':'⚙️')+'</button></div>'}
function nav(){var a=[['home','⌂','Inicio'],['cup','🌋','Cup'],['rank','🏆','Ranking'],['teams','🛡️','Equipos'],['players','👤','Jugadores']];return '<div class="nav"><div class="navInner">'+a.map(function(x){return '<button class="'+(S.tab===x[0]&&!S.admin?'on':'')+'" onclick="go(\''+x[0]+'\')"><span>'+x[1]+'</span>'+x[2]+'</button>'}).join('')+'</div></div>'}
function shell(x){return '<div class="app">'+top()+x+'</div>'+nav()}
function home(){
var p=pool(),p1=Math.round(p*.6),p2=Math.round(p*.25),p3=p-p1-p2;
return shell('<div class="hero"><div class="eyebrow"><i class="dot"></i> REGISTRO ABIERTO</div><h1>VOLCANO #001</h1><div class="sub">THE AWAKENING · 10 equipos · 100 jugadores</div><div class="poolLabel">LIVE PRIZE POOL</div><div class="pool">'+euro(p)+' <span>/ 1.500 €</span></div><div class="bar"><i style="width:'+S.checked+'%"></i></div><div class="stats"><div class="stat"><b>'+S.checked+'/100</b><small>checked-in</small></div><div class="stat"><b>10/10</b><small>equipos</small></div><div class="stat"><b>25</b><small>partidos</small></div></div></div>'+
'<div class="section"><div class="sectionHead"><h2>El dinero</h2><span>17 € / jugador</span></div><div class="card"><div class="moneyRow"><div><b>Campo</b><div class="muted">2 € × '+S.checked+'</div></div><b>'+euro(field())+'</b></div><div class="moneyRow"><div><b>Premios</b><div class="muted">15 € × '+S.checked+'</div></div><b>'+euro(p)+'</b></div></div></div>'+
'<div class="section"><div class="sectionHead"><h2>Podio</h2><span>100% del bote</span></div><div class="card">'+pod('m1','1','Campeón','60%',p1)+pod('m2','2','Subcampeón','25%',p2)+pod('m3','3','Tercer puesto','15%',p3)+'</div></div>'+
'<div class="section"><div class="sectionHead"><h2>Defending the Crater</h2></div><div class="card"><div class="rankRow"><div class="left"><div class="teamIcon">⚔️</div><div><b>Titan FC</b><div class="muted">Campeón anterior</div></div></div><div class="amount">1 🌋</div></div></div></div>');
}
function pod(c,n,t,sub,a){return '<div class="moneyRow"><div class="left"><div class="medal '+c+'">'+n+'</div><div><b>'+t+'</b><div class="muted">'+sub+' del bote</div></div></div><div class="amount">'+euro(a)+'</div></div>'}
function table(g){
var ns=teams.filter(function(t){return t.g===g}).map(function(t){return t.n}),m={};ns.forEach(function(n){m[n]={n:n,pj:0,gf:0,ga:0,pts:0}});
matches[g].forEach(function(x){var a=m[x[0]],b=m[x[1]],sa=x[2],sb=x[3];if(sa==null)return;a.pj++;b.pj++;a.gf+=sa;a.ga+=sb;b.gf+=sb;b.ga+=sa;if(sa>sb)a.pts+=3;else if(sb>sa)b.pts+=3;else{a.pts++;b.pts++}});
return Object.values(m).sort(function(a,b){return b.pts-a.pts||((b.gf-b.ga)-(a.gf-a.ga))||b.gf-a.gf})
}
function cup(){
var body='<h1 class="screenTitle">The Climb</h1><p class="screenSub">Liguilla → Eruption → Semifinales → The Crater</p><div class="tabs"><button class="tab '+(S.group==='A'?'on':'')+'" onclick="setGroup(\'A\')">Grupo A</button><button class="tab '+(S.group==='B'?'on':'')+'" onclick="setGroup(\'B\')">Grupo B</button><button class="tab '+(S.group==='P'?'on':'')+'" onclick="setGroup(\'P\')">Playoffs</button></div>';
if(S.group==='P')body+=bracket();else{var r=table(S.group);body+='<div class="table"><div class="tr head"><div>#</div><div>Equipo</div><div>PJ</div><div>GF</div><div>DG</div><div>Pts</div></div>'+r.map(function(x,i){return '<div class="tr '+(i===0?'q1':i<3?'q2':'out')+'"><div>'+(i+1)+'</div><div class="name">'+icon(x.n)+' '+x.n+'</div><div>'+x.pj+'</div><div>'+x.gf+'</div><div>'+((x.gf-x.ga)>0?'+':'')+(x.gf-x.ga)+'</div><b>'+x.pts+'</b></div>'}).join('')+'</div><div class="section"><div class="sectionHead"><h2>Resultados</h2></div>'+matches[S.group].map(match).join('')+'</div>'}
return shell(body)
}
function match(x){return '<div class="match"><div class="matchLine"><div>'+icon(x[0])+' '+x[0]+'</div><div class="score">'+(x[2]==null?'—':x[2]+'-'+x[3])+'</div><div class="r">'+x[1]+' '+icon(x[1])+'</div></div></div>'}
function block(title,arr){return '<div class="round">'+title+'</div>'+arr.map(function(x){var played=x[2]!=null;return '<div class="match"><div class="'+(played&&x[2]>x[3]?'winner':played?'loser':'')+'">'+icon(x[0])+' '+x[0]+' <b style="float:right">'+(x[2]==null?'—':x[2])+'</b></div><div class="'+(played&&x[3]>x[2]?'winner':played?'loser':'')+'" style="margin-top:8px">'+icon(x[1])+' '+x[1]+' <b style="float:right">'+(x[3]==null?'—':x[3])+'</b></div></div>'}).join('')}
function bracket(){return '<div class="bracket">'+block('ERUPTION',playoffs.eruption)+block('SEMIFINALES',playoffs.semi)+block('LAST MONEY · 3ER PUESTO',playoffs.third)+block('THE CRATER · FINAL',playoffs.final)+'</div>'}
function ranking(){
var a=teams.slice().sort(function(x,y){return S.rank==='rank'?y.pts-x.pts:y.money-x.money});
return shell('<h1 class="screenTitle">Volcano Board</h1><p class="screenSub">El historial no se reinicia cuando termina una Cup.</p><div class="tabs"><button class="tab '+(S.rank==='rank'?'on':'')+'" onclick="setRank(\'rank\')">Volcano Rank</button><button class="tab '+(S.rank==='money'?'on':'')+'" onclick="setRank(\'money\')">Money Board</button></div><div class="card">'+a.map(function(t,i){return '<div class="rankRow"><div class="left"><div style="width:24px;color:var(--muted)">#'+(i+1)+'</div><div class="teamIcon">'+t.i+'</div><div><b>'+t.n+'</b><div class="muted">'+t.cups+' Crater Wins</div></div></div><div style="text-align:right;font-weight:900">'+(S.rank==='rank'?t.pts+' pts':euro(t.money))+'</div></div>'}).join('')+'</div>')
}
function teamsView(){return shell('<h1 class="screenTitle">10 Teams</h1><p class="screenSub">7 titulares + 3 suplentes. Roster bloqueado al empezar.</p><div class="teamGrid">'+teams.map(function(t){return '<div class="teamCard" onclick="teamModal('+t.id+')"><div class="teamIcon">'+t.i+'</div><b>'+t.n+'</b><small>Grupo '+t.g+' · '+t.cups+' títulos</small></div>'}).join('')+'</div>')}
function playersView(){var names=['Adrián Torres','Hugo Vega','Marco Ramos','Dani Suárez','Leo Acosta','Álex Medina','Izan Cruz','Raúl León','Mario Mora','Nico Pérez'];return shell('<h1 class="screenTitle">Players</h1><p class="screenSub">Golden Boot · asistencias · MVP · earnings</p><div class="card">'+names.concat(names.map(function(n){return n+' II'})).map(function(n,i){return '<div class="playerRow"><div><b>#'+(i+1)+' '+n+'</b><div class="muted">'+(19-i%8)+' goles · '+(8-i%5)+' asist.</div></div><span class="pill '+(i<12?'paid':'')+'">'+(i<12?'VERIFIED':'PENDING')+'</span></div>'}).join('')+'</div>')}
function admin(){
var body='<h1 class="screenTitle">Organizer Mode</h1><p class="screenSub">Check-in · efectivo · resultados · roster lock</p><div class="adminNotice">Esta preview guarda los cambios en este iPhone.</div><div class="section"><div class="card"><div class="moneyRow"><div><b>Checked-in</b></div><b>'+S.checked+'/100</b></div><div class="moneyRow"><div><b>Prize Pool</b></div><b>'+euro(pool())+'</b></div><div class="moneyRow"><div><b>Campo</b></div><b>'+euro(field())+'</b></div></div></div><div class="section"><div class="sectionHead"><h2>Control rápido</h2></div><div class="card"><div class="playerRow"><div><b>Simular check-in</b><div class="muted">+1 jugador · 17 € cash</div></div><button class="check on" onclick="addCheck()">+ PAGADO</button></div><div class="playerRow"><div><b>Quitar último check-in</b></div><button class="check" onclick="removeCheck()">−1</button></div><div class="playerRow"><div><b>Editar marcador</b><div class="muted">Desde Match Center</div></div><button class="check" onclick="scoreModal()">EDITAR</button></div></div></div>';
return shell(body)
}
function teamModal(id){var t=teams[id];modal('<button class="close" onclick="closeModal()">×</button><div class="teamIcon">'+t.i+'</div><h3>'+t.n+'</h3><div class="muted">Grupo '+t.g+' · '+t.cups+' Crater Wins · '+euro(t.money)+' career earnings</div><div class="section card"><div class="playerRow"><b>Plantilla</b><span class="pill paid">10/10 LOCKED</span></div><div class="playerRow"><span>Volcano Rank</span><b>'+t.pts+' pts</b></div></div>')}
function scoreModal(){var x=matches.A[0];modal('<button class="close" onclick="closeModal()">×</button><h3>Editar marcador</h3><div class="muted">'+x[0]+' vs '+x[1]+'</div><input id="sa" class="input" type="number" min="0" value="'+x[2]+'"><input id="sb" class="input" type="number" min="0" value="'+x[3]+'"><button class="primary" onclick="saveScore()">GUARDAR RESULTADO</button>')}
function saveScore(){var a=parseInt(document.getElementById('sa').value,10),b=parseInt(document.getElementById('sb').value,10);if(a>=0&&b>=0){matches.A[0][2]=a;matches.A[0][3]=b;closeModal();render()}}
function modal(h){document.body.insertAdjacentHTML('beforeend','<div class="modalBg" onclick="if(event.target===this)closeModal()"><div class="modal">'+h+'</div></div>')} function closeModal(){var x=document.querySelector('.modalBg');if(x)x.remove()}
function go(t){S.tab=t;S.admin=false;save();render()} function setGroup(g){S.group=g;save();render()} function setRank(r){S.rank=r;save();render()} function toggleAdmin(){S.admin=!S.admin;save();render()} function addCheck(){if(S.checked<100)S.checked++;save();render()} function removeCheck(){if(S.checked>0)S.checked--;save();render()}
function render(){var r=document.getElementById('root');r.innerHTML=S.admin?admin():S.tab==='home'?home():S.tab==='cup'?cup():S.tab==='rank'?ranking():S.tab==='teams'?teamsView():playersView()}
render();