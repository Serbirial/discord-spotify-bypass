// save the orignial open function
XMLHttpRequest.prototype.realOpen = XMLHttpRequest.prototype.open
// create a new function to filter out certain urls 
var myOpen = function(method, url, async, user, password) {
  if (url == 'https://api.spotify.com/v1/me/player/pause') {
    url = '127.0.0.1:42069/go/fuck/yourself'
  }
  this.realOpen (method, url, async, user, password)
}
// overwrite the original open with the modded version
XMLHttpRequest.prototype.open = myOpen
