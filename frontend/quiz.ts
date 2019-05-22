// let fd = new FormData();
// fd.append('fatc', this.image);
let url = "http://localhost:5000/api/fact";

async function getFacts(){
    await $.ajax({
        url: url,
        type: "get",
        beforeSend: () => {
            // show gif
        },
        success: (response) => {
           console.log("Received response: ", response);
        },
        error: function (jqXHR, textStatus, errorThrow) {
            alert(textStatus);
        },
        timeout: 8000
    });
}
