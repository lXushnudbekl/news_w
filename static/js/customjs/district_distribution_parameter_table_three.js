$(document).ready(function() {
    $('.expense-decryption').click(function(event) {
        event.preventDefault(); // Prevent the default link behavior

        var parentRow = $(this).closest('tr');
        var groupId = parentRow.data('group-id');
        var subrows = $('.subrow-' + groupId);

        if (!subrows.hasClass('loaded')) {
            // Subrows are not loaded, create them
            $.ajax({
                url: parentRow.data('href-template'), // URL from the data-href-template attribute
                type: 'POST',
                data: {
                    group_id: groupId,
                    csrfmiddlewaretoken: getCsrfToken()
                },
                success: function(response) {
                    var data = response.data;
                    var subrowContent = '';

                    // Build subrow content
                    subrowContent +=
                        '<tr style="background:white;color: grey" class="subrow subrow-' + groupId + '">' +
                        '<td class="sub_row_td" rowspan="2"></td>' +
                        '<td class="sub_row_td" rowspan="2"></td>' +
                        '<td class="sub_row_td" rowspan="2"></td>' +
                        '<td class="sub_row_td hidden" data-month="1" data-quarter="1">' + formatCurrencyWithoutSymbolWithSpaces(data.january.amount) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="2" data-quarter="1">' + formatCurrencyWithoutSymbolWithSpaces(data.february.amount) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="3" data-quarter="1">' + formatCurrencyWithoutSymbolWithSpaces(data.march.amount) + '</td>' +
                        '<td rowspan="2"></td>' +
                        '<td class="sub_row_td hidden" data-month="4" data-quarter="2">' + formatCurrencyWithoutSymbolWithSpaces(data.april.amount) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="5" data-quarter="2">' + formatCurrencyWithoutSymbolWithSpaces(data.may.amount) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="6" data-quarter="2">' + formatCurrencyWithoutSymbolWithSpaces(data.june.amount) + '</td>' +
                        '<td rowspan="2"></td>' +
                        '<td class="sub_row_td hidden" data-month="7" data-quarter="3">' + formatCurrencyWithoutSymbolWithSpaces(data.july.amount) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="8" data-quarter="3">' + formatCurrencyWithoutSymbolWithSpaces(data.august.amount) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="9" data-quarter="3">' + formatCurrencyWithoutSymbolWithSpaces(data.september.amount) + '</td>' +
                        '<td rowspan="2"></td>' +
                        '<td class="sub_row_td hidden" data-month="10" data-quarter="4">' + formatCurrencyWithoutSymbolWithSpaces(data.october.amount) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="11" data-quarter="4">' + formatCurrencyWithoutSymbolWithSpaces(data.november.amount) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="12" data-quarter="4">' + formatCurrencyWithoutSymbolWithSpaces(data.december.amount) + '</td>' +
                        '</tr>' +
                        '<tr style="background:white;color: grey" class="subrow subrow-' + groupId + '">' +
                        '<td class="sub_row_td hidden" data-month="1" data-quarter="1">' + formatCurrencyWithoutSymbolWithSpaces(data.january.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="2" data-quarter="1">' + formatCurrencyWithoutSymbolWithSpaces(data.february.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="3" data-quarter="1">' + formatCurrencyWithoutSymbolWithSpaces(data.march.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="4" data-quarter="2">' + formatCurrencyWithoutSymbolWithSpaces(data.april.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="5" data-quarter="2">' + formatCurrencyWithoutSymbolWithSpaces(data.may.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="6" data-quarter="2">' + formatCurrencyWithoutSymbolWithSpaces(data.june.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="7" data-quarter="3">' + formatCurrencyWithoutSymbolWithSpaces(data.july.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="8" data-quarter="3">' + formatCurrencyWithoutSymbolWithSpaces(data.august.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="9" data-quarter="3">' + formatCurrencyWithoutSymbolWithSpaces(data.september.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="10" data-quarter="4">' + formatCurrencyWithoutSymbolWithSpaces(data.october.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="11" data-quarter="4">' + formatCurrencyWithoutSymbolWithSpaces(data.november.limit) + '</td>' +
                        '<td class="sub_row_td hidden" data-month="12" data-quarter="4">' + formatCurrencyWithoutSymbolWithSpaces(data.december.limit) + '</td>' +
                        '<td class="sub_row_td" rowspan="2"></td>' +
                        '<td class="sub_row_td" rowspan="2"></td>' +
                        '</tr>';

                    // Append subrow content to the DOM after parentRow
                    parentRow.after(subrowContent);
                    console.log("click qilindi",subrowContent)

                    // Sync subrow visibility with the main table column state
                    syncSubrowVisibility(0,0);

                    // Toggle the 'loaded' class to mark subrows as loaded and show them
                    $('.subrow-' + groupId).addClass('loaded').show();
                },
                error: function(xhr, status, error) {
                    console.error('AJAX request error:', error);
                }
            });
        } else {
            // Subrows exist, toggle visibility
            subrows.toggle();
        }
    });
});
function syncSubrowVisibility(quarter, startIndex) {
    let table = document.getElementById("monthly_distribution_table");

    if (quarter !== 0 || startIndex !== 0) {
        // Define the range of months for the given quarter
        const monthsPerQuarter = {
            1: [1, 2, 3], // For Q1
            2: [5, 6, 7], // For Q2
            3: [9, 10, 11], // For Q3
            4: [13, 14, 15]  // For Q4
        };

        let months = monthsPerQuarter[quarter];
        console.log(months)

        // Toggle visibility of the specified months within the specific subrow
        months.forEach(monthIndex => {
            console.log(monthIndex)
            let cells = table.querySelectorAll('.subrow-expense > td[data-month="' + monthIndex + '"]');
            cells.forEach(cell => {
                if (cell.classList.contains("sub_row_td") && cell.dataset.quarter == quarter) {
                    cell.classList.toggle("hidden");
                }
            });
        });
    }
    let cells = table.querySelectorAll('.sub_row_td');

    cells.forEach(cell => {
        cell.classList.remove("hidden"); // Ensure all cells are visible
    });
}
