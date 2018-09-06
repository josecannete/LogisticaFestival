function edit_activity_capacity() {
    var id = $("#id_tabs").val();
    if (id == null) {
        append_alert("warning", "Escoja una actividad");
        return false;
    }
    var cant_act = parseInt($("#ca_value").val());
    var cant_tot = parseInt($("#ct_value").html());
    if (cant_tot < cant_act) {
        append_alert("warning", "No puede existir sobrecapacidad!");
        return false
    }
    var form = $("#edit_capacity_form").serialize();
    $.ajax({
        type: 'POST',
        url: '/edit_activity_capacity/',
        data: form,
        success: function (data) {
            if (data["status"]) {
                append_alert("success", "Información de actividad actualizada");
                setTimeout(function () {
                    location = self.location.href
                }, 1000);
            } else {
                append_alert("warning", data["msg"]);
            }
        }
    });
}

function append_alert(type_alert, msg) {
    var myNode = document.getElementById("div_for_alert");
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