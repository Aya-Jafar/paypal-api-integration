

var updateBtns = document.getElementsByClassName('update-cart')// will store all the buttons tags

for (let i = 0; i < updateBtns.length; i++) {

    updateBtns[i].addEventListener(
        'click',
        function () {
            var productID = this.dataset.product_id // 'this' refers to the element we're listenining to 
            var action = this.dataset.action

            // console.log(productID, action)

            if (currentUser === 'AnonymousUser') {
                console.log('Not logged in')
            }
            else {
                updateUserCard(productID, action)
            }
        }
    )
}


function updateUserCard(productID, action) {
    console.log('User is authenticated , making a POST request to update user card .... ')

    console.log(productID, action)

    var path = '/update-item/' // path to send data to 

    fetch(path, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        // Sending data as a string 
        body: JSON.stringify({
            'productID': productID,
            'action': action
        })
    })  // Sending back data as a JSON to views.py which sends it to the template
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            // console.log(data)
            location.reload()
        });
}






