function fetchAndPrint(printUrl) {
    fetch(printUrl)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Failed to fetch print content');
            }
            return response.text(); // Parse the response as HTML content
        })
        .then((htmlContent) => {

            // Open a new window for printing
            const printWindow = window.open('', '_blank', 'width=800,height=600');
            printWindow.document.open();
            printWindow.document.write(`
                <html>
                    <head>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                padding: 20px;
                            }
                            .table {
                                width: 100%;
                                border-collapse: collapse;
                            }
                            .table th, .table td {
                                padding: 8px;
                                border: 1px solid #ddd;
                            }
                            .card {
                             border: none;
                             border-radius: 8px;background-color: #fff;margin-bottom: 20px;box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);



}
                            }


.card-header {
  font-size: 12px;
  font-weight: bold;
  background-color: #f1f3f5;
  padding: 10px 15px;
  border-bottom: none;
}

                            .table-sm td, .table-sm th {
  padding: 0.3rem;

  word-wrap: break-word;
  white-space: nowrap;
}

.group-cell {
  text-align: center; /* Horizontally center the content */
  vertical-align: middle; /* Vertically center the content */
  color: white; /* Text color */
  background-color: #3a525e; /* Background color (adjust as needed) */
  font-weight: bold; /* Optional: Make text bold */
}

.group-cell a {
  color: white; /* Ensure the link text is also white */
  text-decoration: none; /* Optional: Remove underline from the link */
}


/*signing */

.table-borderless-custom > tbody > th > td {
  border: none;
}

/* Vertically align all items in the row */
.align-items-end {
  display: flex;
  align-items: end;
}

/* Align content to the end (right) */
.justify-content-end {
  justify-content: flex-end;
}

/* Align content to the start (left) */
.justify-content-start {
  justify-content: flex-start;
}

/* Center the QR code */
.text-center {
  text-align: center;
}


/*.pdf-container {*/
/*  display: flex;*/
/*  justify-content: center;*/
/*  align-items: center;*/
/*  !*height: 100vh;*!*/
/*  !*width: 100%;*!*/
/*  padding: 20px;*/
/*  box-sizing: border-box;*/
/*}*/

.content {
  width: 80%;
  margin: 0 auto;
  border: 1px solid #ddd;
  padding: 20px;
  background: #f9f9f9;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}
                            /* More custom styles as needed */
                        </style>
                    </head>
                    <body>
                        ${htmlContent}
                    </body>
                </html>
            `);
            printWindow.document.close();

            // Trigger the print dialog
            printWindow.print();

            // Close the window after printing
            printWindow.onafterprint = () => {
                printWindow.close();
            };
        })
        .catch((error) => {
            console.error('Error while printing:', error);
        });
}
