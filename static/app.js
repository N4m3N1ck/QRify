/*
* This software is licensed under the Creative Commons
* Attribution-NonCommercial 4.0 International License.
* To view a copy of this license, visit
* https://creativecommons.org/licenses/by-nc/4.0/
*/
function copyToClipBoard(id) {
  // Get the text field
  var copyText = document.getElementById(id);
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);
}