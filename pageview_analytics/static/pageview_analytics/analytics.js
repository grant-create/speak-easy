// Reports how long this page was actually visible, not how long the tab
// was open. A tab left in the background overnight should not become a
// ten-hour reading session -- only time while document.visibilityState is
// "visible" accumulates.
(function () {
  var vid = window.__pvaVid;
  var endpoint = window.__pvaBeacon;
  if (!vid || !endpoint) return;

  var accumulated = 0;
  var visibleSince = document.visibilityState === 'visible' ? Date.now() : null;

  function tick() {
    if (visibleSince === null) return accumulated;
    return accumulated + (Date.now() - visibleSince);
  }

  function report(useBeacon) {
    var seconds = Math.round(tick() / 1000);
    if (seconds <= 0) return;

    var payload = JSON.stringify({ vid: vid, seconds: seconds });

    if (useBeacon && navigator.sendBeacon) {
      var blob = new Blob([payload], { type: 'application/json' });
      navigator.sendBeacon(endpoint, blob);
    } else {
      var xhr = new XMLHttpRequest();
      xhr.open('POST', endpoint, false); // synchronous: only used on unload
      xhr.setRequestHeader('Content-Type', 'application/json');
      try { xhr.send(payload); } catch (e) {}
    }
  }

  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible') {
      visibleSince = Date.now();
    } else {
      accumulated = tick();
      visibleSince = null;
      report(true);
    }
  });

  window.addEventListener('pagehide', function () {
    report(true);
  });

  // Safety net in case the final report is lost (crash, force-quit).
  setInterval(function () { report(true); }, 60000);
})();
