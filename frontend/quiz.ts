// let fd = new FormData();
// fd.append('fatc', this.image);
let url = "http://localhost:5000/api/fact";

async function getFacts(){
    await $.ajax({
        url: url,
        type: "get",
        headers: {
            'Access-Control-Allow-Origin': 'http://localhost:5000',
        },
        beforeSend: () => {
            // show gif
        },
        success: (response) => {
           console.log("Received response: ", response);
        },
        error: function (jqXHR, textStatus, errorThrow) {
            // alert(textStatus);
            alert(errorThrow);
        },
        timeout: 8000
    });
}
