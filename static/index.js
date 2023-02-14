const courses = document.querySelectorAll('.course');

  courses.forEach(course => {
    const teacher = course.nextElementSibling;
    const desc = teacher.nextElementSibling;


  course.addEventListener('click', () => {
    if (teacher.style.display === 'none' && desc.style.display === 'none') {
        teacher.style.display = 'block';
        desc.style.display = 'block';
      } else {
        teacher.style.display = 'none';
        desc.style.display = 'none';
      }
    });
});