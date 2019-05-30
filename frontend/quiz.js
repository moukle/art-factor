let base_url = "http://localhost:5000/api/fact";
// let base_url = "http://192.168.99.100:5000/api/fact";

async function getFacts2(){
    const response = await fetch(base_url);
    const data = await response.json();

    data.forEach(el=>{
        const {Fact} = el;
        const {factTrue, object, predicate, resource, subject} = Fact;
    });
}

// async function getFacts(){
//     await $.ajax({
//         url: base_url,
//         type: "get",
//         beforeSend: () => {
//             // show gif
//         },
//         success: (response) => {
//             alert(response)
//             console.log("Received response: ", response);
//         },
//         error: function (jqXHR, textStatus, errorThrow) {
//             alert(textStatus);
//         }
//     });
// }