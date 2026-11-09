(() => {
 const cfg = window.LAB_CONFIG || {}, params = new URLSearchParams(location.search);
 let active = false;
 const safeGet = (key) => { try { return localStorage.getItem(key); } catch { return null; } };
 const safeSet = (key,value) => { try { localStorage.setItem(key,value); } catch {} };
 const gaOK = /^G-[A-Z0-9]+$/.test(cfg.ga4 || '');
 const ymOK = /^\d+$/.test(String(cfg.metrica || '')) && Number(cfg.metrica)>0;
 const allowed = new Set(['cta_click','demo_start','demo_step','demo_complete','request_start','demo_request']);
 function init() {
  if(active) return; active=true;
  if(gaOK) {
   window.dataLayer=window.dataLayer||[];
   window.gtag=function(){window.dataLayer.push(arguments)};
   gtag('js',new Date());
   const options={send_page_view:true,allow_google_signals:false,allow_ad_personalization_signals:false};
   if(params.get('debug')==='1') options.debug_mode=true;
   gtag('config',cfg.ga4,options);
   const script=document.createElement('script');script.async=true;script.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(cfg.ga4);document.head.append(script);
  }
  if(ymOK) {
   window.ym=window.ym||function(){(window.ym.a=window.ym.a||[]).push(arguments)};window.ym.l=Date.now();
   const script=document.createElement('script');script.async=true;script.src='https://mc.yandex.ru/metrika/tag.js';document.head.append(script);
   ym(Number(cfg.metrica),'init',{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:false});
  }
 }
 window.labTrack=(name,details={})=>{
  if(!active||!allowed.has(name))return;
  // Never send form values, identifiers or arbitrary caller-provided parameters.
  const p={page_type:'student_demo'};
  if(['hero','section','request'].includes(details.placement))p.placement=details.placement;
  if(Number.isInteger(details.step)&&details.step>=1&&details.step<=3)p.step=details.step;
  if(gaOK)gtag('event',name,p);
  if(ymOK)ym(Number(cfg.metrica),'reachGoal',name,p);
 };
 const banner=document.getElementById('consent');
 if(safeGet('lab_analytics_consent_v1')==='yes')init();
 else if(safeGet('lab_analytics_consent_v1')!=='no')banner.hidden=false;
 document.getElementById('consent-yes').onclick=()=>{safeSet('lab_analytics_consent_v1','yes');banner.hidden=true;init()};
 document.getElementById('consent-no').onclick=()=>{safeSet('lab_analytics_consent_v1','no');banner.hidden=true;if(active)location.reload()};
 document.getElementById('privacy-settings').onclick=()=>{banner.hidden=false};
})();
