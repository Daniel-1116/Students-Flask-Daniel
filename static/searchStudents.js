
// searching the students

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
      
      var nameAnchor = name.querySelector("a");

      if (nText.includes(keyword) || eText.includes(keyword) || cText.includes(keyword)) {
        row.style.display = "";
        highlightText(nameAnchor, keyword);
      } else {
        row.style.display = "none";
      }
    }
  }
});

function highlightText(anchor, keyword) {
  var text = anchor.textContent;
  var regex = new RegExp(keyword, "gi");
  var highlightedText = text.replace(regex, '<span style="background-color: yellow;">$&</span>');
  anchor.innerHTML = highlightedText;
}
