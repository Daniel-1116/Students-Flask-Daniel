
const profilePictureContainer = document.querySelector('.profile-picture-container');
const editIcon = document.querySelector('.edit-icon');
const uploadPhotoForm = document.querySelector('.upload-photo-form');
const fileInput = document.querySelector('input[type="file"]');

profilePictureContainer.addEventListener('mouseenter', () => {
    editIcon.style.display = 'block';
});

profilePictureContainer.addEventListener('mouseleave', () => {
    editIcon.style.display = 'none';
});

editIcon.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    uploadPhotoForm.submit();
});