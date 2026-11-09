(() => {
 const track=document.getElementById('carousel-track');
 if(!track)return;
 const prev=document.getElementById('carousel-prev'),next=document.getElementById('carousel-next'),status=document.getElementById('carousel-status');
 const count=track.children.length;
 const position=()=>Math.min(count-1,Math.max(0,Math.round(track.scrollLeft/Math.max(1,track.clientWidth))));
 function update(){const i=position();prev.disabled=i===0;next.disabled=i===count-1;status.textContent='Карточка '+(i+1)+' из '+count;}
 function move(delta){const i=Math.min(count-1,Math.max(0,position()+delta));track.scrollTo({left:i*track.clientWidth,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}
 prev.addEventListener('click',()=>move(-1));next.addEventListener('click',()=>move(1));
 track.addEventListener('scroll',update,{passive:true});
 track.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();move(e.key==='ArrowRight'?1:-1)}});
 window.addEventListener('resize',update);update();
})();
