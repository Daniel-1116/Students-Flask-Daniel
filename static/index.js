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


function filterTable() {
  console.log("Filtering table...");
  
  // Get the search keyword entered by the user
  var input = document.getElementById("search-input");
  var keyword = input.value.toLowerCase();

  // Get the table rows and loop through them
  var table = document.getElementById("students-table");
  var rows = table.getElementsByTagName("tr");
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];

    // Get the student name from the first column
    var name = row.getElementsByTagName("td")[0];
    if (name) {
      var text = name.textContent.toLowerCase();
      
      // If the search keyword is found in the student name, show the row, otherwise hide it
      if (text.indexOf(keyword) > -1) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    }
  }
}
