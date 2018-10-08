function append_alert(type_alert, msg, div_id = 'div_for_alert') {
    var myNode = document.getElementById(div_id);
    while (myNode.firstChild) {
        myNode.removeChild(myNode.firstChild);
    }
    myNode.appendChild(generate_alert(type_alert, msg));
}

function generate_alert(type_alert, msg) {
    return htmlToElement('<div class="alert alert-dismissible fade show alert-' + type_alert + '" role="alert" id="alert_div"><div id="alert_msg">' + msg + '</div><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>');
}

function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

function myFunction(){
    console.log("form submitted!")
}

$('#new_tour_form').on('submit', function(event) {
        console.log("form submitted!")
        var $this = $(document.getElementById("load"));
      $this.button('loading');
        setTimeout(function() {
           $this.button('reset');
       }, 8000);
});