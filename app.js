(function(){
"use strict";
var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
function clamp(v,a,b){return v<a?a:v>b?b:v}

/* ---------- spring (semi-implicit Euler, fixed substeps) ---------- */
function Spring(x,k,zeta){this.x=x;this.v=0;this.t=x;this.set(k,zeta)}
Spring.prototype.set=function(k,zeta){this.k=k;this.c=2*zeta*Math.sqrt(k)};
Spring.prototype.step=function(dt){var n=Math.max(1,Math.ceil(dt/0.008)),h=dt/n;for(var i=0;i<n;i++){var a=this.k*(this.t-this.x)-this.c*this.v;this.v+=a*h;this.x+=this.v*h}};
Spring.prototype.rest=function(){return Math.abs(this.t-this.x)<0.0005&&Math.abs(this.v)<0.0005};
function rubber(over,dim){var c=0.55;return (over*dim*c)/(dim+c*Math.abs(over))}
/* velocity tracker over the last ~100ms of pointer samples */
function Tracker(){this.s=[]}
Tracker.prototype.add=function(x,y){var t=performance.now();this.s.push([t,x,y]);while(this.s.length>2&&t-this.s[0][0]>100)this.s.shift()};
Tracker.prototype.vel=function(){var s=this.s;if(s.length<2)return[0,0];var a=s[0],b=s[s.length-1],dt=(b[0]-a[0])/1000;if(dt<=0)return[0,0];if(performance.now()-b[0]>80)return[0,0];return[(b[1]-a[1])/dt,(b[2]-a[2])/dt]};

/* ---------- star-tile pattern, drawn once, used by the bow tie and the floor ---------- */
function tileCanvas(){
  var c=document.createElement("canvas");c.width=c.height=256;var g=c.getContext("2d"),s=128;
  g.fillStyle="#ece8e1";g.fillRect(0,0,256,256);
  for(var ty=0;ty<2;ty++)for(var tx=0;tx<2;tx++){
    var ox=tx*s,oy=ty*s,cx=ox+s/2,cy=oy+s/2;
    g.strokeStyle="#8f928f";g.lineWidth=3;g.beginPath();g.moveTo(cx,oy+5);g.lineTo(ox+s-5,cy);g.lineTo(cx,oy+s-5);g.lineTo(ox+5,cy);g.closePath();g.stroke();
    g.fillStyle="#1b1d1f";g.beginPath();
    for(var i=0;i<8;i++){var a=i*Math.PI/4-Math.PI/2,r=i%2===0?s*0.40:s*0.10;g.lineTo(cx+Math.cos(a)*r,cy+Math.sin(a)*r)}
    g.closePath();g.fill();
    g.fillStyle="#ece8e1";g.beginPath();g.arc(cx,cy,s*0.045,0,Math.PI*2);g.fill();
  }
  g.fillStyle="#1b1d1f";
  for(var y=0;y<=256;y+=s)for(var x=0;x<=256;x+=s){g.beginPath();g.moveTo(x,y-15);g.lineTo(x+15,y);g.lineTo(x,y+15);g.lineTo(x-15,y);g.closePath();g.fill()}
  return c;
}
var tiles=tileCanvas();
try{var tf=document.getElementById("tileFloor");tf.style.backgroundImage="url("+tiles.toDataURL("image/png")+")"}catch(e){}

/* ---------- white brick texture for the price wall ---------- */
(function(){
  try{
    var c=document.createElement("canvas");c.width=360;c.height=168;var g=c.getContext("2d");
    g.fillStyle="#cbc3b7";g.fillRect(0,0,360,168);
    var seed=7;function rnd(){seed=(seed*16807)%2147483647;return seed/2147483647}
    for(var row=0;row<4;row++){
      var off=row%2?-90:0;
      for(var x=off;x<360;x+=180){
        var l=226+Math.floor(rnd()*12),hue=Math.floor(rnd()*6);
        g.fillStyle="rgb("+(l)+","+(l-4-hue)+","+(l-10-hue)+")";
        g.fillRect(x+3,row*42+3,174,36);
        g.fillStyle="rgba(255,255,255,.18)";g.fillRect(x+3,row*42+3,174,4);
      }
    }
    var el=document.getElementById("brick");el.style.backgroundImage="url("+c.toDataURL("image/png")+")";
  }catch(e){}
})();

/* ---------- live open / closed status in Cyprus time ---------- */
var HOURS=[null,[540,1080],[540,1080],[540,1080],null,[540,1080],[540,1050]];
var DAYS=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
function hm(m){var h=Math.floor(m/60),mm=m%60;return(h<10?"0":"")+h+":"+(mm<10?"0":"")+mm}
function cyprusNow(){
  try{
    var f=new Intl.DateTimeFormat("en-GB",{timeZone:"Asia/Nicosia",weekday:"short",hour:"2-digit",minute:"2-digit",hourCycle:"h23"});
    var p={};f.formatToParts(new Date()).forEach(function(x){p[x.type]=x.value});
    var d=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].indexOf(p.weekday);
    return{day:d,min:(+p.hour%24)*60+(+p.minute)};
  }catch(e){var n=new Date();return{day:n.getDay(),min:n.getHours()*60+n.getMinutes()}}
}
function updateStatus(){
  var n=cyprusNow(),h=HOURS[n.day],open=false,text;
  if(h&&n.min>=h[0]&&n.min<h[1]){open=true;var left=h[1]-n.min;text=left<=45?"Open, closes in "+left+" min":"Open until "+hm(h[1])}
  else if(h&&n.min<h[0]){text="Closed, opens "+hm(h[0])}
  else{for(var k=1;k<=7;k++){var d=(n.day+k)%7;if(HOURS[d]){text="Closed till "+(k===1?"tomorrow":DAYS[d].slice(0,3))+" "+hm(HOURS[d][0]);break}}}
  var st=document.getElementById("status");
  st.classList.toggle("is-open",open);st.classList.toggle("is-closed",!open);
  var stx=document.getElementById("statusText");if(stx.textContent!==text)stx.textContent=text;
  document.getElementById("nowLine").textContent="It’s "+hm(n.min)+" on "+DAYS[n.day]+" in Larnaca. "+(open?"We’re open.":"We’re closed right now.");
  var lis=document.querySelectorAll("#hoursList li");
  for(var i=0;i<lis.length;i++)lis[i].classList.toggle("today",+lis[i].getAttribute("data-d")===n.day);
}
updateStatus();setInterval(updateStatus,30000);

/* ---------- header edge + phone action bar ---------- */
var top=document.getElementById("top"),bar=document.getElementById("bar");
function measureHeader(){document.documentElement.style.setProperty("--hdr",top.offsetHeight+"px")}
measureHeader();window.addEventListener("resize",measureHeader);
var heroCtas=document.getElementById("heroCtas"),findSec=document.getElementById("find");
var ctaVisible=true,findVisible=false,doorVisible=false;
function syncBar(){var show=!ctaVisible&&!findVisible&&!doorVisible;bar.classList.toggle("show",show);bar.setAttribute("aria-hidden",show?"false":"true");bar.querySelectorAll("a").forEach(function(a){a.tabIndex=show?0:-1});document.documentElement.style.setProperty("--barpad",show?"72px":"0px")}
if("IntersectionObserver"in window){
  new IntersectionObserver(function(e){ctaVisible=e[0].isIntersecting;syncBar()}).observe(heroCtas);
  new IntersectionObserver(function(e){findVisible=e[0].isIntersecting;syncBar()},{rootMargin:"0px 0px -30% 0px"}).observe(findSec);
  if(!reduce)new IntersectionObserver(function(e){doorVisible=e[0].isIntersecting;syncBar()},{rootMargin:"-20% 0px -20% 0px"}).observe(document.getElementById("walkTrack"));
}
window.addEventListener("scroll",function(){top.classList.toggle("scrolled",window.scrollY>8)},{passive:true});

/* ---------- copy the phone number ---------- */
var copyBtn=document.getElementById("copyBtn"),copyLabel=document.getElementById("copyLabel"),copyIcon=document.getElementById("copyIcon");
var COPY_ICON=copyIcon.innerHTML,CHECK_ICON='<path d="M20 6 9 17l-5-5"/>',copyTimer;
function setCopy(label,icon){copyBtn.classList.add("swap");setTimeout(function(){copyLabel.textContent=label;copyIcon.innerHTML=icon;copyBtn.classList.remove("swap")},110)}
function selectPhone(){var r=document.createRange();r.selectNodeContents(document.getElementById("phone"));var s=getSelection();s.removeAllRanges();s.addRange(r)}
copyBtn.addEventListener("click",function(){
  clearTimeout(copyTimer);
  var done=function(){setCopy("Copied",CHECK_ICON);copyTimer=setTimeout(function(){setCopy("Copy number",COPY_ICON)},2200)};
  var fail=function(){selectPhone();setCopy("Number selected, copy it",COPY_ICON);copyTimer=setTimeout(function(){setCopy("Copy number",COPY_ICON)},3200)};
  try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText("+357 97 782071").then(done,fail)}else fail()}catch(e){fail()}
});

/* ---------- the bow tie (three.js r128) ---------- */
(function(){
  var wrap=document.getElementById("tieWrap"),canvas=document.getElementById("tie"),hint=document.getElementById("tieHint");
  function fallback(){canvas.hidden=true;document.getElementById("tieFallback").hidden=false;hint.hidden=true}
  if(typeof THREE==="undefined"){fallback();return}
  var renderer;
  try{renderer=new THREE.WebGLRenderer({canvas:canvas,antialias:true,alpha:true});}catch(e){fallback();return}
  if(!renderer||!renderer.getContext()){fallback();return}
  renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
  renderer.outputEncoding=THREE.sRGBEncoding;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
  var scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(28,1,0.1,60);

  var tex=new THREE.CanvasTexture(tiles);tex.wrapS=tex.wrapT=THREE.RepeatWrapping;tex.encoding=THREE.sRGBEncoding;tex.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
  var wingMat=new THREE.MeshStandardMaterial({map:tex,roughness:.64,metalness:.02,side:THREE.DoubleSide});
  var knotMat=new THREE.MeshStandardMaterial({color:new THREE.Color(0xedb12a).convertSRGBToLinear(),roughness:.55,metalness:.04});

  function wing(dir){
    var U=60,V=56,L=1.22,H=.72,T=.16,pos=[],uv=[],idx=[];
    for(var i=0;i<=U;i++){
      var u=i/U;
      var ph=(.2+.8*Math.pow(u,.55));                       /* pinched at the knot, flared at the tip */
      if(u>.88)ph*=Math.sqrt(1-Math.pow((u-.88)/.12,2)*.14);
      var pt=(.5+.5*Math.sin(Math.PI*Math.min(1,u*1.15)))*Math.sqrt(Math.max(0,1-Math.pow(u,7)));
      for(var j=0;j<=V;j++){
        var v=j/V*Math.PI*2,cy=Math.cos(v),sz=Math.sin(v);
        var y=H*ph*cy;
        var z=T*pt*sz*(1+.45*u*Math.sin(cy*Math.PI*3.2));   /* pleats running out from the knot */
        var x=L*u*(1-.12*u*(1-Math.abs(cy)));
        z-=.2*u*u;                                          /* wings sweep back */
        pos.push(dir*x,y,z);uv.push(u*1.6,j/V*2.6);
      }
    }
    for(i=0;i<U;i++)for(j=0;j<V;j++){var a=i*(V+1)+j,b=a+V+1,c=a+1,d=b+1;if(dir>0)idx.push(a,c,b,b,c,d);else idx.push(a,b,c,b,d,c)}
    var geo=new THREE.BufferGeometry();
    geo.setAttribute("position",new THREE.Float32BufferAttribute(pos,3));
    geo.setAttribute("uv",new THREE.Float32BufferAttribute(uv,2));
    geo.setIndex(idx);geo.computeVertexNormals();return geo;
  }
  var tie=new THREE.Group();
  tie.add(new THREE.Mesh(wing(1),wingMat));tie.add(new THREE.Mesh(wing(-1),wingMat));
  var kg=new THREE.SphereGeometry(1,48,32),kp=kg.attributes.position;
  for(var i=0;i<kp.count;i++){var x=kp.getX(i),y=kp.getY(i),z=kp.getZ(i),f=1+.07*Math.sin(y*9)*(1-Math.abs(y));kp.setXYZ(i,x*.22*f,y*.3,z*.2*f+.03)}
  kg.computeVertexNormals();
  tie.add(new THREE.Mesh(kg,knotMat));
  tie.rotation.z=-.04;
  scene.add(tie);

  scene.add(new THREE.HemisphereLight(0xc9d6e0,0x2a2016,.55));
  var key=new THREE.SpotLight(0xffe2b4,2.2,30,Math.PI/5,.6,1.2);key.position.set(.6,5,4.5);scene.add(key);key.target=tie;
  var rim=new THREE.PointLight(0xa47dff,1.6,12,1.6);rim.position.set(-3.2,.6,-2.2);scene.add(rim);
  var fill=new THREE.DirectionalLight(0x9fb4c4,.35);fill.position.set(3,-1,3);scene.add(fill);

  function resize(){
    var w=wrap.clientWidth,h=wrap.clientHeight;if(!w||!h)return;
    renderer.setSize(w,h,false);camera.aspect=w/h;
    var vfov=camera.fov*Math.PI/180,hfov=2*Math.atan(Math.tan(vfov/2)*camera.aspect);
    var needW=3.25,needH=1.95;
    var dist=Math.max((needW/2)/Math.tan(hfov/2),(needH/2)/Math.tan(vfov/2));
    camera.position.set(0,.18,dist);camera.lookAt(0,.02,0);camera.updateProjectionMatrix();
  }
  resize();
  if("ResizeObserver"in window)new ResizeObserver(resize).observe(wrap);else window.addEventListener("resize",resize);

  /* physics: rotation follows the finger on springs, momentum on release */
  var rotY=new Spring(-.5,70,.9),rotX=new Spring(0,90,.62),drop=new Spring(reduce?0:1.4,90,.72);
  drop.t=0;
  var idleW=0,momentum=0,dragging=false,startX=0,startY=0,baseY=0,baseX=0,intent=null,pid=null,tr=new Tracker(),touched=false;
  canvas.addEventListener("pointerdown",function(e){
    if(dragging||e.button>0)return;
    pid=e.pointerId;intent=null;startX=e.clientX;startY=e.clientY;baseY=rotY.t;baseX=rotX.t;momentum=0;tr.s=[];tr.add(e.clientX,e.clientY);dragging=true;
  });
  canvas.addEventListener("pointermove",function(e){
    if(!dragging||e.pointerId!==pid)return;
    var dx=e.clientX-startX,dy=e.clientY-startY;
    if(!intent){if(Math.abs(dx)>8&&Math.abs(dx)>Math.abs(dy)){intent="spin";try{canvas.setPointerCapture(pid)}catch(_){ }canvas.classList.add("dragging");if(!touched){touched=true;hint.classList.add("gone")}}else if(Math.abs(dy)>10){dragging=false;return}else return}
    tr.add(e.clientX,e.clientY);
    rotY.t=baseY+dx*.011;
    rotX.t=rubber(baseX+dy*.006,.5);
  });
  function end(e){
    if(!dragging||(e&&e.pointerId!==pid))return;dragging=false;canvas.classList.remove("dragging");
    if(intent!=="spin")return;
    var v=tr.vel();var w=v[0]*.011;
    if(!reduce){momentum=clamp(w,-22,22);rotY.v+=momentum*.5}
    rotX.t=0;
  }
  canvas.addEventListener("pointerup",end);canvas.addEventListener("pointercancel",end);canvas.addEventListener("lostpointercapture",end);

  var last=performance.now(),visible=true,running=false;
  function frame(now){
    var dt=Math.min(.05,(now-last)/1000);last=now;
    if(!dragging){
      if(Math.abs(momentum)>.05){rotY.t+=momentum*dt;momentum*=Math.exp(-2.1*dt)}else momentum=0;
      var targetIdle=reduce?0:(Math.abs(momentum)<.6?.42:0);
      idleW+=(targetIdle-idleW)*Math.min(1,dt*1.5);
      rotY.t+=idleW*dt;
    }else idleW=0;
    rotY.step(dt);rotX.step(dt);drop.step(dt);
    tie.rotation.y=rotY.x;tie.rotation.x=rotX.x+.08;tie.position.y=drop.x;
    renderer.render(scene,camera);
    if(visible&&!document.hidden)requestAnimationFrame(frame);else running=false;
  }
  function start(){if(!running){running=true;last=performance.now();requestAnimationFrame(frame)}}
  if("IntersectionObserver"in window)new IntersectionObserver(function(e){visible=e[0].isIntersecting;if(visible)start()}).observe(wrap);
  document.addEventListener("visibilitychange",function(){if(!document.hidden&&visible)start()});
  start();
  canvas.addEventListener("webglcontextlost",function(e){e.preventDefault();fallback()});
})();

/* ---------- walk in through the door (scroll-driven) ---------- */
(function(){
  if(reduce)return;
  var track=document.getElementById("walkTrack"),stage=document.getElementById("walkStage"),frame=document.getElementById("walkFrame");
  var L=document.getElementById("doorL"),R=document.getElementById("doorR"),inside=document.getElementById("inside"),shade=document.getElementById("shade");
  var A=document.getElementById("capA"),B=document.getElementById("capB");
  function eio(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2}
  var ticking=false;
  function update(){
    ticking=false;
    var r=track.getBoundingClientRect(),sh=stage.offsetHeight,sw=stage.offsetWidth;
    var p=clamp(-r.top/Math.max(1,r.height-sh),0,1);
    var g=eio(clamp(p/.42,0,1));
    var fw=Math.min(sw-48,sh*.62),fh=Math.min(sh-110,fw*1.36);
    var ix=(sw-fw)/2*(1-g),iy=Math.max(20,(sh-fh)*.42)*(1-g),ib=Math.max(20,(sh-fh)-(sh-fh)*.42)*(1-g),rad=18*(1-g);
    frame.style.clipPath="inset("+iy.toFixed(1)+"px "+ix.toFixed(1)+"px "+ib.toFixed(1)+"px "+ix.toFixed(1)+"px round "+rad.toFixed(1)+"px)";
    var o=eio(clamp((p-.38)/.44,0,1));
    var walk=1+.07*g+.05*o;
    L.style.transform="translateX("+(-104*o).toFixed(2)+"%) scale("+walk.toFixed(4)+")";
    R.style.transform="translateX("+(104*o).toFixed(2)+"%) scale("+walk.toFixed(4)+")";
    inside.style.transform="scale("+(1.16-.16*o).toFixed(4)+")";
    shade.style.opacity=(.55*(1-o)).toFixed(3);
    var a=1-clamp((p-.26)/.12,0,1),b=clamp((p-.66)/.12,0,1);
    A.style.opacity=a.toFixed(3);A.style.transform="translateY("+(-14*(1-a)).toFixed(1)+"px)";
    B.style.opacity=b.toFixed(3);B.style.transform="translateY("+(14*(1-b)).toFixed(1)+"px)";
  }
  function req(){if(!ticking){ticking=true;requestAnimationFrame(update)}}
  window.addEventListener("scroll",req,{passive:true});window.addEventListener("resize",req);
  update();
})();

/* ---------- photo ring: drag with momentum, snaps to a photo ---------- */
(function(){
  var stage=document.getElementById("ringStage"),ring=document.getElementById("ring"),cards=[].slice.call(ring.children),cap=document.getElementById("ringCap");
  var N=cards.length,STEP=360/N,R=300,theta=new Spring(0,140,.86),dragging=false,intent=null,pid=null,sx=0,sy=0,base=0,tr=new Tracker(),current=-1,running=false;
  function layout(){
    var w=ring.offsetWidth;R=Math.round((w/2)/Math.tan(Math.PI/N)+w*.12);
    cards.forEach(function(c,i){c.style.transform="rotateY("+(i*STEP)+"deg) translateZ("+R+"px)"});
    paint();
  }
  function paint(){
    ring.style.transform="translateZ("+(-R)+"px) rotateY("+theta.x.toFixed(3)+"deg)";
    for(var i=0;i<N;i++){var a=(i*STEP+theta.x)*Math.PI/180,f=Math.cos(a);cards[i].style.opacity=(f>-.1?(.45+.55*Math.max(0,f)):0).toFixed(3)}
    var idx=((-Math.round(theta.t/STEP))%N+N)%N;
    if(idx!==current){current=idx;cap.textContent=cards[idx].querySelector("img").alt;cards.forEach(function(c,i){c.setAttribute("aria-hidden",i===idx?"false":"true")})}
  }
  var last=0;
  function tick(now){
    var dt=Math.min(.05,(now-last)/1000);last=now;
    if(reduce&&!dragging){theta.x=theta.t;theta.v=0}else theta.step(dt);
    paint();
    if(dragging||!theta.rest())requestAnimationFrame(tick);else{theta.x=theta.t;paint();running=false}
  }
  function kick(){if(!running){running=true;last=performance.now();requestAnimationFrame(tick)}}
  function go(d){theta.set(140,.86);theta.t=Math.round(theta.t/STEP)*STEP+d*STEP;kick()}
  document.getElementById("ringPrev").addEventListener("click",function(){go(1)});
  document.getElementById("ringNext").addEventListener("click",function(){go(-1)});
  stage.addEventListener("keydown",function(e){if(e.key==="ArrowLeft"){go(1);e.preventDefault()}else if(e.key==="ArrowRight"){go(-1);e.preventDefault()}});
  stage.addEventListener("pointerdown",function(e){if(dragging||e.button>0)return;dragging=true;intent=null;pid=e.pointerId;sx=e.clientX;sy=e.clientY;base=theta.x;tr.s=[];tr.add(e.clientX,e.clientY)});
  function resnap(){theta.set(110,.82);theta.t=Math.round(theta.t/STEP)*STEP;kick()}
  stage.addEventListener("pointermove",function(e){
    if(!dragging||e.pointerId!==pid)return;
    var dx=e.clientX-sx,dy=e.clientY-sy;
    if(!intent){if(Math.abs(dx)>8&&Math.abs(dx)>Math.abs(dy)){intent="turn";try{stage.setPointerCapture(pid)}catch(_){ }stage.classList.add("dragging");base=theta.x;sx=e.clientX;theta.set(260,1);kick()}else if(Math.abs(dy)>10){dragging=false;resnap();return}else return}
    tr.add(e.clientX,e.clientY);
    theta.t=base+(e.clientX-sx)/R*180/Math.PI;
  });
  function end(e){
    if(!dragging||(e&&e.pointerId!==pid))return;dragging=false;stage.classList.remove("dragging");
    if(intent!=="turn"){resnap();return}
    var w=tr.vel()[0]/R*180/Math.PI;                     /* deg per second */
    var projected=theta.x+(w/1000)*.995/(1-.995);         /* Apple's momentum projection, deceleration .995 */
    theta.set(110,.82);theta.t=Math.round(projected/STEP)*STEP;theta.v=w;kick();
  }
  stage.addEventListener("pointerup",end);stage.addEventListener("pointercancel",end);stage.addEventListener("lostpointercapture",end);
  layout();
  if("ResizeObserver"in window)new ResizeObserver(layout).observe(ring);else window.addEventListener("resize",layout);
})();
})();
