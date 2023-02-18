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


// function filterTable() {
//   console.log("Filtering table...");
  
  const input = document.getElementById("search-input");
  input.addEventListener('input', () => {
  var keyword = input.value.toLowerCase();

  var table = document.getElementById("students-table");
  var rows = table.getElementsByTagName("tr");
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var name = row.getElementsByTagName("td")[0];
    var email = row.getElementsByTagName("td")[1];
    var course = row.getElementsByTagName("td")[2];
    if (name && email && course) {
      var nText = name.textContent.toLowerCase();
      var eText = email.textContent.toLowerCase();
      var cText = course.textContent.toLowerCase();
      

      if (nText.indexOf(keyword) > -1 || eText.indexOf(keyword) > -1 || cText.indexOf(keyword) > -1) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    }
  }
})
