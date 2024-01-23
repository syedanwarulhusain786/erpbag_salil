  // JavaScript code to handle the modal


 // Function to open the "Add New Primary Group" modal
 function openAddNewModal() {
    document.getElementById('accountModal').style.display = 'block';
    console.log('e')
  }

  // Function to close the "Add New Primary Group" modal
  function closeAddNewModal() {
    document.getElementById('accountModal').style.display = 'none';
    console.log('w')

  }

  // Event listener for the "Add New Primary Group" button
  document.getElementById('openModalBtn').addEventListener('click', openAddNewModal);

  // Event listener for the modal close button
  document.getElementById('closeModalBtn').addEventListener('click', closeAddNewModal);
  document.getElementById('closeModalBtn1').addEventListener('click', closeAddNewModal);

   


function DeleteAction(action, rowId, accountname) {
    
    // Handle the response based on the action
    
       // Populate and display the confirmation modal
    const closebt = document.getElementById("closeModals");
    const nobt = document.getElementById("cancelDeleteBtn");
    const conf = document.getElementById("confirmDeleteBtn");

    document.getElementById("confirmationModal").style.display = "block";

    document.getElementById("accountNumberc").value = rowId;
    document.getElementById("accountNamec").value = accountname;
    closebt.addEventListener("click", function () {
      document.getElementById("confirmationModal").style.display =  "none";
        accountForm.reset();
    });
    nobt.addEventListener("click", function () {
      document.getElementById("confirmationModal").style.display =  "none";
        accountForm.reset();
    });






  // Function to handle form submission (you can customize this according to your needs)





 


    // You can also submit the form data to the Django backend using AJAX or a form submission, depending on your preference.
};