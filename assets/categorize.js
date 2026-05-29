window.APWH = window.APWH || {};
APWH.initCategorize = function(root, opts){
  opts = opts || {};
  var snapParent = opts.snapParent || null;
  var onProgress = opts.onProgress || function(){};
  var zones = [].slice.call(root.querySelectorAll('.zone'));
  var chips = [].slice.call(root.querySelectorAll('.chip'));
  var total = chips.length, solved = 0;
  var armed = null, drag = null, suppressClick = false;

  function setArmed(chip){
    if (armed) armed.classList.remove('armed');
    armed = (chip === armed) ? null : chip;
    if (armed) armed.classList.add('armed');
  }
  function answersFor(chip){ return (chip.dataset.answers || '').split(',').filter(Boolean); }

  function snap(chip, zone, point){
    var pr = snapParent.getBoundingClientRect();
    snapParent.appendChild(chip);
    chip.classList.add('snapped');
    var cw = chip.offsetWidth, ch = chip.offsetHeight, x, y;
    if (point){ x = point.x - pr.left; y = point.y - pr.top; }
    else { var zr = zone.getBoundingClientRect(); x = zr.left - pr.left + zr.width/2; y = zr.top - pr.top + zr.height/2; }
    x += (Math.random()*16-8); y += (Math.random()*10-5);
    x = Math.max(2, Math.min(pr.width - cw - 2, x - cw/2));
    y = Math.max(2, Math.min(pr.height - ch - 2, y - ch/2));
    chip.style.position='absolute'; chip.style.left = x+'px'; chip.style.top = y+'px';
  }

  function place(chip, zone, point){
    if (chip.classList.contains('placed')) return;
    if (answersFor(chip).indexOf(zone.dataset.zone) !== -1){
      chip.classList.remove('armed','bad'); chip.classList.add('placed');
      chip.setAttribute('aria-disabled','true');
      if (snapParent) snap(chip, zone, point);
      else (zone.querySelector('.zchips') || zone).appendChild(chip);
      armed = null; solved++; onProgress(solved, total);
    } else {
      chip.classList.add('bad');
      setTimeout(function(){ chip.classList.remove('bad'); }, 480);
    }
  }

  zones.forEach(function(z){
    z.addEventListener('click', function(){ if (suppressClick) return; if (armed) place(armed, z, null); });
  });
  chips.forEach(function(chip){
    chip.addEventListener('click', function(){ if (suppressClick) return; if (!chip.classList.contains('placed')) setArmed(chip); });
    chip.addEventListener('pointerdown', function(e){
      if (chip.classList.contains('placed')) return;
      var r = chip.getBoundingClientRect();
      drag = { chip:chip, dx:e.clientX-r.left, dy:e.clientY-r.top, w:r.width, x0:e.clientX, y0:e.clientY, moved:false };
      chip.setPointerCapture(e.pointerId);
    });
    chip.addEventListener('pointermove', function(e){
      if (!drag || drag.chip !== chip) return;
      if (!drag.moved && Math.abs(e.clientX-drag.x0)+Math.abs(e.clientY-drag.y0) < 6) return;
      if (!drag.moved){ drag.moved = true; chip.classList.add('dragging'); chip.style.width = drag.w+'px'; }
      chip.style.left = (e.clientX-drag.dx)+'px';
      chip.style.top = (e.clientY-drag.dy)+'px';
      var el = document.elementFromPoint(e.clientX, e.clientY);
      var z = el && el.closest ? el.closest('.zone') : null;
      zones.forEach(function(zo){ zo.classList.toggle('hot', zo===z); });
    });
    function end(e){
      if (!drag || drag.chip !== chip) return;
      var moved = drag.moved; drag = null;
      zones.forEach(function(zo){ zo.classList.remove('hot'); });
      if (moved){
        chip.classList.remove('dragging'); chip.style.left=chip.style.top=chip.style.width='';
        var el = document.elementFromPoint(e.clientX, e.clientY);
        var z = el && el.closest ? el.closest('.zone') : null;
        if (z) place(chip, z, {x:e.clientX, y:e.clientY});
        suppressClick = true; setTimeout(function(){ suppressClick = false; }, 60);
      }
    }
    chip.addEventListener('pointerup', end);
    chip.addEventListener('pointercancel', function(){ if(drag){ drag.chip.classList.remove('dragging'); drag.chip.style.left=drag.chip.style.top=drag.chip.style.width=''; drag=null; } });
  });
  onProgress(0, total);
};
