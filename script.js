$(document).ready(function () {
    console.log("ready");
    var table = $("#tableBody");
    var subjects = $("#subjectSelect");

    $.getJSON("./course_catalog.json", function (data) {
        for (var subject in data) {
            subjects.append('<option value="' + subject + '">' + subject + '</option>');

            for (var course in data[subject]) {
                var c = data[subject][course];
                var row = '<tr data-subject="' + subject + '">';
                row += '<th scope="row" class="courseNumber">';
                row += subject + c.n;
                row += '</th>';
                row += '<td class="courseTitle">';
                row += c.t;
                row += '</td>';
                row += '<td class="courseCredits">';
                row += c.c;
                row += '</td></tr>';

                table.append(row);
            }
        }
    });
});

function search() {
    var input, filter, table, tr, x;
    input = document.getElementById("search");
    filter = input.value.toLowerCase().split(' ');
    table = document.getElementById("courseTable");
    tr = table.getElementsByTagName("tr");

    var subject = $("#subjectSelect").val();
    console.log("subject: " + subject);

    for (x = 0; x < tr.length; x++) {
        var row, title, num;
        row = tr[x];
        title = row.getElementsByClassName("courseTitle")[0];
        num = row.getElementsByClassName("courseNumber")[0];


        if (title || num) {
            title = title.innerHTML.toLowerCase();
            num = num.innerHTML.toLowerCase();
            if (
                (filter.every(v => title.includes(v)) || filter.every(v => num.includes(v)))
                /*((title.indexOf(filter) > -1) || (num.indexOf(filter) > -1))*/
                && (row.dataset.subject == subject || subject == "any")
            ) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        }
    }
}
