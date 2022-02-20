/*************************************************/
/* File: main.js                                 */
/* Author: Dane Rainbird                         */
/* Date: 20/02/2022                              */
/*************************************************/

/**
 * Reads the orders file and parses the orders
 * 
 * @param {*} e event object
 */
function readFile(e) {
    let file = e.target.files[0];
    // If there's no file, then exit
    if (!file) {
        console.error("Failed to load file.");
        alert("Failed to load file. Please try again");
        return;
    }
    // Create the Reader
    var reader = new FileReader();
    
    // Read the file when the Reader is loaded 
    reader.onload = function(e) {
        var contents = e.target.result;
        
        // Parse the orders
        parseOrders(contents);

    };

    // Read the file
    reader.readAsText(file);
}

/**
 * Parses the orders from the file and appends them to the orders list
 * 
 * @param {*} contents data from the file
 */
function parseOrders(contents) {
    // Try JSONify the contents
    try {
        contents = JSON.parse(contents);
        
        // Hide the file input box
        document.getElementById("file-input-box").classList.add("hidden");

    } catch (e) {
        alert("Failed to parse the file. Please ensure you are using a valid JSON file.");
        return;
    }

    // Display the contents of the file
    let ordersElem = document.getElementById("orders");
    ordersElem.classList.remove("hidden");

    // For each order, create a new order object
    for (let i = 0; i < contents.length; i++) {
        let order = contents[i];
        let detailElem = document.createElement("details");
        detailElem.id = "order-" + i;

        let html = ""; 
        html += "<summary>Order on " + order['date'] + "</summary>";
        html += 
        `<div class='order-detail'>
            <p class='order-detail-location'><strong>Location: </strong>` + order['location'] + `</p>
            <p class='order-detail-price'><strong>Total Price: </strong>` + ((order['totalPrice'] != "") ? order['totalPrice'] : "$0.00")  + `</p>
            <p class='order-detail-items-header'><strong>Products:</strong></p>
            <table class='order-detail-items-table'>
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Status</th>
                    </tr>
                </thead>`;

        html += "<tbody>";
        for (let j = 0; j < order['products'].length; j++) {
            let product = order['products'][j];
            html += 
            `<tr>
                <td>` + product['name'] + `</td>
                <td>` + product['status'] + `</td>
            </tr>`;
        }

        html += `</tbody></table>`;
        html += `<a href="` + order['url'] + `" class="order-detail-link-button" target=_blank>View Order</a>`;
        html += `</div>`;

        detailElem.innerHTML = html;

        ordersElem.append(detailElem);
    }
}

/**
 * Event listener for the order search box. When the user types in the search box,
 * the orders are filtered based on the search term (case insensitive).
 */
document.getElementById('orders-search-bar').addEventListener('keyup', function(e) {
    let searchTerm = e.target.value.toLowerCase();
    let orders = document.getElementById("orders");
    let orderElems = orders.getElementsByTagName("details");

    // Check through each order and see if it contains the search term
    for (let i = 0; i < orderElems.length; i++) {
        let orderElem = orderElems[i];
        let order = orderElem.getElementsByClassName("order-detail")[0];
        let orderLocation = order.getElementsByClassName("order-detail-location")[0].innerText.toLowerCase();
        let orderPrice = order.getElementsByClassName("order-detail-price")[0].innerText.toLowerCase();
        let orderItems = order.getElementsByClassName("order-detail-items-table")[0].childNodes[2].innerText.toLowerCase();

        // If the order doesn't contain the search term, hide it
        if (orderLocation.includes(searchTerm) || orderItems.includes(searchTerm) || orderPrice.includes(searchTerm)) {
            orderElem.classList.remove("hidden");
        } else {
            orderElem.classList.add("hidden");
        }
    }
});

/**
 * Event listener for the file input box. When the user selects a file,
 * the file is read and parsed.
 */
document.getElementById('file-upload').addEventListener('change', readFile, false);

/**
 * Event listener for the Floating Help Button. When the user clicks the button,
 * the contents box is swapped for the help box.
 */
document.getElementById('about-fab').addEventListener('click', function() {
    let aboutElem = document.getElementById('about');
    let contentElem = document.getElementById('content');

    // If the about box is hidden, show it, otherwise hide it
    if (aboutElem.classList.contains('hidden')) {
        aboutElem.classList.remove('hidden');
        contentElem.classList.add('hidden');
    } else {
        aboutElem.classList.add('hidden');
        contentElem.classList.remove('hidden');
    }
});