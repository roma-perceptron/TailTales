// notie settings
var notie = window.notie;
notie.setOptions({
  alertTime: 3,
  dateMonths: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
  overlayClickDismiss: true,
  overlayOpacity: 0.75,
  transitionCurve: 'ease',
  transitionDuration: 0.3,
  transitionSelector: 'all',
  positions: {
    alert: 'bottom',
    force: 'bottom',
    confirm: 'bottom',
    input: 'bottom',
    select: 'bottom',
    date: 'bottom'
  }
})

console.log('Base settings loaded..');