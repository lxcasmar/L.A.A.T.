function autocomplete(input, arr) {
  let currentFocus; // current selected autocomplete option
  input.addEventListener("input", function (e) {
    let a,
      b,
      i,
      val = this.value;
    closeAllLists(); // closes the drop down options on update
    if (!val) return false; // if there is nothing entered exit early
    currentFocus = -1;
    // div that holds the autocomplete items
    a = document.createElement("DIV");
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items");
    this.parentNode.appendChild(a);
    // adds the hits to the autocomplete drop down
    for (i = 0; i < arr.length; i++) {
      if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        b = document.createElement("DIV");
        b.innerHTML = `<strong>${arr[i].substr(0, val.length)}</strong>`;
        b.innerHTML += arr[i].substr(val.length);
        b.innerHTML += `<input type='hidden' value='${arr[i]}'>`;
        b.addEventListener("click", function (e) {
          // makes the input value the selected option
          input.value = this.getElementsByTagName("input")[0].value;
          // closes dropdown
          closeAllLists();
        });
        a.appendChild(b);
      }
    }
  });
  input.addEventListener("keydown", function (e) {
    let x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      currentFocus++;
      addActive(x);
    } else if (e.keyCode == 38) {
      currentFocus--;
      addActive(x);
    } else if (e.keyCode == 13) {
      e.preventDefault();
      if (currentFocus > -1) {
        if (x) x[currentFocus].click();
      }
    }
  });
  function addActive(x) {
    if (!x) return false;
    removeActive(x);
    // can probably optimize this to a single calculation
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = x.length - 1;
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(el) {
    let x = document.getElementsByClassName("autocomplete-items");
    for (let i = 0; i < x.length; i++) {
      if (el != x[i] && el != input) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  const selectTicker = document.getElementById("addInput");
  document.addEventListener("click", function (e) {
    if (e.target != selectTicker) closeAllLists(e.target);
  });
  const selectedTickers = [];
  const selectedTickersContainer = document.getElementById("selectedTickers");
  selectTicker.addEventListener("click", function (e) {
    e.preventDefault();
    const currentInput = input.value;
    // exits if max tickers selected, ticker already selected, or no valid input
    if (
      !currentInput ||
      selectedTickers.includes(currentInput) ||
      !arr.includes(currentInput)
    )
      return;
    selectedTickers.push(currentInput);
    const selection = document.createElement("li");
    selection.innerText = currentInput;
    const close = document.createElement("span");
    close.innerText = "x";
    close.setAttribute("class", "close");
    selection.insertAdjacentElement("beforeend", close);
    close.addEventListener("click", function () {
      selectedTickers.splice(selectedTickers.indexOf(currentInput), 1);
      selectedTickersContainer.removeChild(selection);
    });
    //selection.innerHTML = `${currentInput}<span class="close">x</span>`;
    selectedTickersContainer.appendChild(selection);
    closeAllLists();
  });
  document.querySelector("form").onsubmit = function (e) {
    console.log(selectedTickers.length);
    if (selectedTickers.length >= 1) {
      input.setCustomValidity("");
      input.value = JSON.stringify(selectedTickers);
    } else {
      //e.preventDefault();
      // input.setCustomValidity("Please select at least one ticker!");
      // input.reportValidity();
      return false;
    }
  };
}
