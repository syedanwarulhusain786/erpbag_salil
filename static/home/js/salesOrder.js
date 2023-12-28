




// Create a new Date object for today's date
const today = new Date();

// Get the year, month, and day in the format "YYYY-MM-DD"
const year = today.getFullYear();
const month = (today.getMonth() + 1).toString().padStart(2, '0'); // Months are 0-indexed
const day = today.getDate().toString().padStart(2, '0');

// Set the value of the date input to today's date
// dateInput.value = `${year}-${month}-${day}`;
bankjournal_date.value=`${year}-${month}-${day}`;


document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector("#transactionTable tbody");

    tableBody.addEventListener('change', function (event) {
        const dropdown = event.target;
        if (dropdown.tagName === 'SELECT' && dropdown.id.startsWith('dropdown')) {
            const rowNum = dropdown.id.replace('dropdown', '');
            const catInput = document.getElementById(`cat${rowNum}`);
            const subInput = document.getElementById(`ref${rowNum}`);

            const selectedOption = dropdown.options[dropdown.selectedIndex];
            const subcategory = selectedOption.getAttribute('data-tokens');
            const category = selectedOption.getAttribute('data-value');
            // console.log(catInput);

            // console.log(`Selected Account Number for Row ${rowNum}:`, subcategory);
            catInput.value = category;
            subInput.value = subcategory;
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // ...
    // Get a reference to the "Add Row" button
    const addRowButton = document.getElementById("addRowButton");

    // Function to add a new row to the table
    function addNewRow() {
        
        const table = document.getElementById("transactionTable");
        const newRow = table.insertRow(table.rows.length - 3); // Insert before the last row
        const countInput = document.getElementById('count');
        countInput.value = parseInt(countInput.value) + 1;
        // Clone the cells from an existing row (you can choose any row as a template)
        const templateRow = table.rows[1]; // Assuming the second row (index 1) is your template
        for (let i = 0; i < templateRow.cells.length; i++) {
            const newCell = newRow.insertCell(i);
            newCell.innerHTML = templateRow.cells[i].innerHTML;
        }

        // Add a "Remove" button to the new row
        const removeCell = newRow.insertCell(templateRow.cells.length);
        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.classList.add("btn", "btn-danger", "remove-row-button");
        removeButton.textContent = "Remove";
        removeCell.appendChild(removeButton);

        // Attach a click event listener to the "Remove" button
        removeButton.addEventListener("click", function () {
            table.deleteRow(newRow.rowIndex);
            updateRowIds(); // Update the IDs after removing a row
            const countInput = document.getElementById('count');
            countInput.value = parseInt(countInput.value) - 1;
        });

        // Update the IDs of the cloned elements to avoid duplicates
        const rowIndex = table.rows.length - 3; // Index of the new row (0-based)
        const elementsToChange = newRow.querySelectorAll("[id]");
        elementsToChange.forEach(function (element) {
            const id = element.getAttribute("id");
            const idParts = id.split(/\d+/);
            const num = rowIndex; // Adding 1 to match the row number
            element.setAttribute("id", idParts[0] + num);
            element.setAttribute("name", idParts[0] + num); // Also update the 'name' attribute if needed
            // element.value = ""; // Clear the input values in the new row
        });
    }

    // Add a click event listener to the "Add Row" button
    addRowButton.addEventListener("click", addNewRow);

    // Function to update the IDs of all rows after removing a row
    function updateRowIds() {
        const table = document.getElementById("transactionTable");
        for (let i = 1; i < table.rows.length - 1; i++) {
            const row = table.rows[i];
            const elementsToUpdate = row.querySelectorAll("[id]");
            elementsToUpdate.forEach(function (element) {
                const id = element.getAttribute("id");
                const idParts = id.split(/\d+/);
                const num = i - 1; // Subtract 1 to match the row number
                element.setAttribute("id", idParts[0] + num);
                element.setAttribute("name", idParts[0] + num); // Also update the 'name' attribute if needed
            });
        }
    }
});




clearFormButton.addEventListener("click", function () {
    // Reset the form fields to their default values
    const form = document.getElementById("myActualForm");
    const tableRows = form.querySelectorAll("tbody tr");

    tableRows.forEach((row, index) => {
        const select = row.querySelector("select");
        const cat = row.querySelector(`#cat${index + 1}`);
        const ref = row.querySelector(`#ref${index + 1}`);
        const sub = row.querySelector(`#sub${index + 1}`);

        const amt = row.querySelector(`#amt${index + 1}`);
        // const cre = row.querySelector(`#cre${index + 1}`);

        // Clear the form fields
        select.value = ''; // Clear the select value
        cat.value = ''; // Clear the cat input value
        ref.value = ''; // Clear the sub input value
        sub.value = ''; // Clear the nar input value
        amt.value = ''; // Clear the cre input value
        // cre.value = ''; // Clear the deb input value
    });
});
// Update the modal content with data
function updateModalData(data) {
    const account = data.message.account;
    const voucherCode = data.message.voucherCode;
    const voucherNo = data.message.voucherNo;
    const modal = document.getElementById('myModal');
    const closeBtn = document.getElementsByClassName('close')[0];
    const closeBtn1 = document.getElementById('closeModalq');

    const voucherNoElement = document.getElementById('voucherNo');
    const voucherCodeElement = document.getElementById('voucherCode');
    const accountElement = document.getElementById('account');
    voucherNoElement.value = voucherNo;
    voucherCodeElement.value = voucherCode;
    accountElement.value = account;
    modal.style.display = 'block';  // Show the modal

    // Close the modal when the close button is clicked
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';

    });

    closeBtn1.addEventListener('click', () => {
        modal.style.display = 'none';
        const clearFormButton = document.getElementById("clearFormButton");

        // Simulate a click event on the clearFormButton
        clearFormButton.click();
    });
}







document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById('transactionTable');
    const submitButton = document.getElementById('submitForm');

    function calculateAndLogTotals() {
        let creTotal = 0;
        let debTotal = 0;
        let txtotal = 0;

        // Calculate the total of "cre" inputs
        const creInputs = container.querySelectorAll('input[id^="cre"]');
        creInputs.forEach(input => {
            const value2 = parseFloat(input.value) || 0;
            creTotal += value2;
        });

        // Calculate the total of "deb" inputs
        const debInputs = container.querySelectorAll('input[id^="amt"]');
        debInputs.forEach(input => {
            const value1 = parseFloat(input.value) || 0;
            debTotal += value1;
        });

        const total_deb = document.getElementById("d_total");
        total_deb.value = debTotal.toFixed(2);

        const d_tax2 = document.getElementById("d_tax");
        var tx=parseFloat(total_deb.value) || 0;
        var gst=0.18*tx
        // Assuming d_tax2.value contains the VAT value
       

        var amount = parseFloat(total_deb.value) || 0;
        d_tax2.value = gst.toFixed(2);

        var total = amount + gst;

        // Set the calculated values to their respective fields

        const final = document.getElementById("final");
        final.value = total.toFixed(2);
    }

    container.addEventListener("input", calculateAndLogTotals);
});








