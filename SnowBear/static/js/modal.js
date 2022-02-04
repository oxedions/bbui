document.addEventListener('DOMContentLoaded', () => {

    // Get all dropdowns on the page that aren't hoverable.
    const dropdowns = document.querySelectorAll('.dropdown:not(.is-hoverable)');

    if (dropdowns.length > 0) {
      // For each dropdown, add event handler to open on click.
      dropdowns.forEach(function(el) {
        el.addEventListener('click', function(e) {
        closeDropdowns();
          e.stopPropagation();
          el.classList.toggle('is-active');
        });
      });

      // If user clicks outside dropdown, close it.
      document.addEventListener('click', function(e) {
        closeDropdowns();
      });
    }

    /*
    * Close dropdowns by removing `is-active` class.
     */
    function closeDropdowns() {
      dropdowns.forEach(function(el) {
        el.classList.remove('is-active');
      });
    }

    // Close dropdowns if ESC pressed
    document.addEventListener('keydown', function (event) {
      let e = event || window.event;
      if (e.key === 'Esc' || e.key === 'Escape') {
        closeDropdowns();
      }
    });


    // Functions to open and close a modal
    function openModal($el) {
      $el.classList.add('is-active');
    }
  
    function closeModal($el) {
      $el.classList.remove('is-active');
    }
  
    function closeAllModals() {
      (document.querySelectorAll('.modal') || []).forEach(($modal) => {
        closeModal($modal);
      });
    }
  
    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
      const modal = $trigger.dataset.target;
      const $target = document.getElementById(modal);
      console.log($target);
  
      $trigger.addEventListener('click', () => {
        openModal($target);
      });
    });
  
    // Add a click event on various child elements to close the parent modal
    (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
      const $target = $close.closest('.modal');
  
      $close.addEventListener('click', () => {
        closeModal($target);
      });
    });
  
    // Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
      const e = event || window.event;
  
      if (e.keyCode === 27) { // Escape key
        closeAllModals();
      }
    });
  });




