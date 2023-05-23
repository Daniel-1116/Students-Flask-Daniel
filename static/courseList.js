
//courses list

const courses = document.querySelectorAll('.course-info');

courses.forEach(course => {
  course.addEventListener('mouseover', () => {
    const teacher = course.querySelector('.teacher');
    const desc = course.querySelector('.desc');
    teacher.style.display = 'block';
    desc.style.display = 'block';
  });

  course.addEventListener('mouseout', () => {
    const teacher = course.querySelector('.teacher');
    const desc = course.querySelector('.desc');
    teacher.style.display = 'none';
    desc.style.display = 'none';
  });
});