"use strict";

function toCurrency(inputEl: HTMLInputElement): void {
    const float = parseFloat(inputEl.value)
    if (!isNaN(float)) {
        inputEl.value = float.toFixed(2);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const bidEl = document.getElementById("id-bid");
    if (bidEl === null) {
        return;
    }
    const bidInput = <HTMLInputElement>bidEl;
    toCurrency(bidInput)
    bidInput.addEventListener("change", (): void => {
        toCurrency(bidInput);
    });
});
