window.APWH = window.APWH || {};
(function(){
  var base = (typeof window.APWH_BASE === 'string') ? window.APWH_BASE : '';
  APWH.unitId = function(){ return new URLSearchParams(location.search).get('unit') || 'unit1'; };
  APWH.mediaBase = base;
  APWH.load = function(cb){
    var id = APWH.unitId();
    if (APWH[id]) { cb(APWH[id], id); return; }
    var s = document.createElement('script');
    s.src = base + 'data/' + id + '.js';
    s.onload = function(){ cb(APWH[id], id); };
    s.onerror = function(){ document.body.innerHTML = '<div class="wrap"><p>Could not load vocabulary data for "' + id + '". Make sure the site is opened through its web address, not as a bare file.</p></div>'; };
    document.head.appendChild(s);
  };
  APWH.audioSrc = function(unit, term){ return base + 'audio/' + unit.id + '/' + term.audio; };
  // Reuse one persistent Audio element. A locally-scoped `new Audio()` can be
  // garbage-collected mid-play in Firefox (you hear nothing); a kept reference
  // avoids that and lets a new click interrupt the previous clip cleanly.
  var _audio = null;
  APWH.play = function(unit, term){
    if (!term || !term.audio) return;
    try {
      var src = APWH.audioSrc(unit, term);
      if (!_audio) _audio = new Audio();
      _audio.src = src;
      _audio.currentTime = 0;
      var p = _audio.play();
      if (p && p.catch) p.catch(function(e){ console.warn('APWH audio play failed:', src, e); });
    } catch(e){ console.warn('APWH audio error:', e); }
  };
  APWH.shuffle = function(a){ a = a.slice(); for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;} return a; };
  APWH.sample = function(arr, n, exclude){
    var pool = arr.filter(function(x){ return x !== exclude; });
    return APWH.shuffle(pool).slice(0, n);
  };
})();
