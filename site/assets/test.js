(function(){
var T=window.TEST,KEY='kat-'+T.id,$=function(s){return document.querySelector(s)};
var st=load(); 
function load(){try{return JSON.parse(localStorage.getItem(KEY))||{}}catch(e){return{}}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
function wc(t){return (t.trim().match(/\S+/g)||[]).length}
function esc(s){return s.replace(/[&<>]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
var L='ABCD';
function render(){
  var h='',n=0;
  T.sections.forEach(function(s){
    h+='<div class="sec">'+s.name+'</div>';
    s.qs.forEach(function(q){n++;q._n=n;
      h+='<div class="q" id="q'+n+'"><div class="n">Question '+n+'</div><div>'+q.q+'</div>';
      q.o.forEach(function(o,i){h+='<label class="opt" id="o'+n+'_'+i+'"><input type="radio" name="q'+n+'" value="'+i+'"'+(st.ans&&st.ans[n]===i?' checked':'')+'>'+L[i]+'. '+o+'</label>'});
      h+='<div id="x'+n+'"></div></div>'});
  });
  var w=T.writing;
  h+='<div class="sec">Writing Skills</div><div class="q"><div class="n">Essay · not more than 300 words</div><div>'+w.prompt+'</div><p><textarea id="essay" placeholder="Write your response here…">'+esc(st.essay||'')+'</textarea></p><div class="wc" id="wc"></div><div id="wx"></div></div>';
  $('#paper').innerHTML=h;
  var e=$('#essay');function upd(){var c=wc(e.value);$('#wc').textContent=c+' / 300 words';$('#wc').className='wc'+(c>300?' over':'')}
  upd();e.addEventListener('input',function(){st.essay=e.value;save();upd()});
  document.querySelectorAll('#paper input[type=radio]').forEach(function(r){r.addEventListener('change',function(){
    var q=+r.name.slice(1);st.ans=st.ans||{};st.ans[q]=+r.value;save();prog()})});
  prog();
}
function prog(){var a=Object.keys(st.ans||{}).length,t=T.sections.reduce(function(s,x){return s+x.qs.length},0);$('#prog').textContent=a+' / '+t+' answered'}
function fmt(s){var m=Math.floor(s/60),x=s%60;return m+':'+(x<10?'0':'')+x}
function tick(){
  if(st.state!=='running')return;st=load();if(st.state!=='running')return;
  var left=Math.round((st.deadline-Date.now())/1000);
  if(left<=0){$('#clock').textContent='0:00';submit(true);return}
  $('#clock').textContent=fmt(left);$('#clock').className=left<300?'low':'';
}
function start(){st={state:'running',deadline:Date.now()+T.minutes*60000,ans:{},essay:''};save();show();}
function show(){
  $('#gate').hidden=true;$('#runbar').hidden=false;$('#paper').hidden=false;$('#submit').hidden=false;render();tick();window._t=setInterval(tick,1000);
}
function submit(auto){
  st=load();var t=T.sections.reduce(function(s,x){return s+x.qs.length},0),a=Object.keys(st.ans||{}).length;
  if(!auto&&a<t&&!confirm((t-a)+' question(s) are unanswered. Submit anyway?'))return;
  st.state='done';save();clearInterval(window._t);mark();
}
function mark(){
  $('#gate').hidden=true;$('#paper').hidden=false;$('#runbar').hidden=true;$('#submit').hidden=true;
  if(!$('#q1'))render();
  var tot=0,max=0,by=[];
  T.sections.forEach(function(s){var sc=0;s.qs.forEach(function(q){
    max++;var n=q._n,pick=st.ans&&st.ans[n];
    document.querySelectorAll('input[name=q'+n+']').forEach(function(i){i.disabled=true});
    $('#o'+n+'_'+q.a).classList.add('right');
    if(pick===q.a){sc++;tot++}else if(pick!==undefined)$('#o'+n+'_'+pick).classList.add('wrong');
    $('#x'+n).innerHTML='<div class="sol"><span class="ans">Answer: '+L[q.a]+'. '+q.o[q.a]+'</span>'+(pick===undefined?' <i>(not attempted)</i>':'')+'<br>'+q.s+'</div>';
  });by.push([s.name,sc,s.qs.length])});
  var w=T.writing,c=wc(st.essay||'');
  $('#wx').innerHTML='<div class="sol"><b>Self-assess your essay</b> ('+c+' words'+(c>300?' – over the limit':'')+'). Tick what you achieved:<ul style="list-style:none;padding:0">'+w.rubric.map(function(r){return '<li><label><input type="checkbox"> <b>'+r[0]+'</b> – '+r[1]+'</label></li>'}).join('')+'</ul><details class="a"><summary>Planning notes and a model response</summary><ul>'+w.plan.map(function(p){return '<li>'+p+'</li>'}).join('')+'</ul><p>'+w.model+'</p></details></div>';
  var h='<div class="q"><div class="score">'+tot+' / '+max+'</div><table><tr><th>Section</th><th>Score</th></tr>'+by.map(function(b){return '<tr><td>'+b[0]+'</td><td>'+b[1]+' / '+b[2]+'</td></tr>'}).join('')+'</table><p class="note">The essay is not auto-marked. No negative marking is applied here (Krea has not published its scheme).</p><div class="tools"><button id="again" class="ghost">Retake this test</button></div></div>';
  $('#result').innerHTML=h;$('#result').hidden=false;window.scrollTo(0,0);
  $('#again').onclick=function(){if(confirm('Clear your answers and start again?')){try{localStorage.removeItem(KEY)}catch(e){}location.reload()}};
}
$('#begin').onclick=start;$('#submit').onclick=function(){submit(false)};
if(st.state==='running'){if(st.deadline<=Date.now()){st.state='done';save();mark()}else show()}
else if(st.state==='done')mark();
})();
