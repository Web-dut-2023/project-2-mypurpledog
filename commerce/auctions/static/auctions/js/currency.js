"use strict";
function toCurrency(inputEl) {
    const float = parseFloat(inputEl.value);
    if (!isNaN(float)) {
        inputEl.value = float.toFixed(2);
    }
}
document.addEventListener("DOMContentLoaded", () => {
    const bidEl = document.getElementById("id-bid");
    if (bidEl === null) {
        return;
    }
    const bidInput = bidEl;
    toCurrency(bidInput);
    bidInput.addEventListener("change", () => {
        toCurrency(bidInput);
    });
});
