document.addEventListener('DOMContentLoaded', () => {
  const mobileToggle = document.querySelector('.js-mobile-toggle');
  const mobileMenu = document.querySelector('.js-mobile-menu');

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('show');
    });
  }

  document.querySelectorAll('.dropdown').forEach(dropdown => {
    const toggle = dropdown.querySelector('.dropdown-toggle');
    const label = dropdown.querySelector('.dropdown-label');
    const hiddenInput = dropdown.querySelector('input[type="hidden"]');
    const form = dropdown.closest('form');
    const autoSubmit = dropdown.dataset.autosubmit === 'true';

    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      document.querySelectorAll('.dropdown.open').forEach(d => {
        if (d !== dropdown) d.classList.remove('open');
      });
      dropdown.classList.toggle('open');
    });

    dropdown.querySelectorAll('.dropdown-item').forEach(item => {
      item.addEventListener('click', () => {
        hiddenInput.value = item.dataset.value;
        label.textContent = item.textContent;
        dropdown.querySelectorAll('.dropdown-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');
        dropdown.classList.remove('open');
        if (autoSubmit && form) form.submit();
      });
    });
  });

  document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown.open').forEach(d => d.classList.remove('open'));
  });

  const fileInput = document.querySelector('.file-upload input[type="file"]');
  const fileLabel = document.getElementById('file-upload-label');
  if (fileInput && fileLabel) {
    fileInput.addEventListener('change', () => {
      fileLabel.textContent = fileInput.files.length
        ? fileInput.files[0].name
        : 'Rasm tanlash';
    });
  }
});