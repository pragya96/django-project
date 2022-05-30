function get_html(fieldName, fieldId, value) {
    if (["quantity", "price"].includes(fieldName)) {
        var fieldType = 'number';
    } else if ("availability" == fieldName) {
        var fieldType = 'select';
        var options = JSON.parse(availability);
    } else if ("store" == fieldName) {
        var fieldType = 'select';
        var options = JSON.parse(stores);
    } else if ("category" == fieldName) {
        var fieldType = 'select';
        var options = JSON.parse(categories);
    } else {
        var fieldType = 'text';
    }

    if (fieldType == 'select') {
        var html = "<select data-id='" + fieldId + "' class='input-field form-control' name='" + fieldName + "'>";
        jQuery.each(options, function(index, item) {
            html += "<option value='" + index + "' ";
            if (value == item) {
                html += "selected";
            }
            html += ">" + item + "</option>";
        });
        html += "</select>";
    } else {
        var html = "<input type='" + fieldType + "' data-id='" + fieldId + "' class='input-field form-control' name='" + fieldName + "' value='" + value + "' >";
    }
    return html
}

$(document).on("click", ".editable", function(e) {
    var fieldName = $(this).attr('data-name');
    var fieldId = $(this).attr('data-id');
    var value = $(this).text();
    var html = get_html(fieldName, fieldId, value);
    $(this).html(html);
    $(this).removeClass("editable");
});

$(document).on("blur", ".input-field", function(e) {
    var html = $(this).parent("td");
    var rowId = $(this).attr('data-id');
    var fieldName = $(this).attr('name');
    if (["availability", "store", "category"].includes(fieldName)) {
        var value = parseInt($(this).val());
    } else {
        var value = $(this).val();
    }
    $data = {
        "csrfmiddlewaretoken": csrf_token,
    }
    $data[fieldName] = value;
    $.ajax({
        type: 'POST',
        url: product_form_url.replace('0', rowId),
        data: $data,
        dataType: "json",
        success: function(response) {
            console.log("Success");
        },
        error: function(response) {
            console.log(response);
        }
    });
    if (["availability", "store", "category"].includes(fieldName)) {
        value = $("option:selected", this).text();
    }
    $(this).remove();
    html.html(value);
    html.addClass("editable");
});

$(document).ready(function() {
    $("#import-product-button").on("click", function() {
        $("#import_product").modal('show');
    });

    $("#import-product-form").on("submit", function(e) {
        e.preventDefault();
        var formData = new FormData();
        formData.append("csrfmiddlewaretoken", csrf_token);
        var f_obj = $("#product-file").get(0).files[0];
        formData.append("file", f_obj);
        $.ajax({
            type: 'POST',
            url: product_import_url,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success");
                window.location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                $("#import_product").modal('hide');
                error_message = xhr.responseJSON;
                alert(error_message.error);
                console.log(error_message);
                console.log(error_message.error);
            }
        });
    });

    $("#create-store-button").on("click", function() {
        $("#store_create").modal('show');
    });

    $("#store_create_form").on("submit", function(e) {
        e.preventDefault();
        var formData = new FormData();
        formData.append("csrfmiddlewaretoken", csrf_token);
        var items_data = {
            "name": $(this).find("#store-name").val()
        };
        formData.append("create_store_data", JSON.stringify(items_data));
        $.ajax({
            type: 'POST',
            url: store_create_url,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success");
                window.location.reload();
            },
            error: function(response) {
                console.log(response);
            }
        });
    });

    $("#create-category-button").on("click", function() {
        $("#category_create").modal('show');
    });

    $("#category_create_form").on("submit", function(e) {
        e.preventDefault();
        var formData = new FormData();
        formData.append("csrfmiddlewaretoken", csrf_token);
        var items_data = {
            "name": $(this).find("#category-name").val()
        };
        formData.append("create_category_data", JSON.stringify(items_data));
        $.ajax({
            type: 'POST',
            url: category_create_url,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success");
                window.location.reload();
            },
            error: function(response) {
                console.log(response);
            }
        });
    });


    $('#datatable').DataTable({
        'serverSide': true,
        'ajax': '/api/product_list/?format=datatables',
        'columnDefs': [{
                "targets": 1,
                createdCell: function(td, cellData, rowData, row, col) {
                    $(td).attr('data-name', 'name');
                    $(td).attr('data-id', rowData['id']);
                    $(td).attr('class', 'editable');
                }
            },
            {
                "targets": 2,
                createdCell: function(td, cellData, rowData, row, col) {
                    $(td).attr('data-name', 'quantity');
                    $(td).attr('data-id', rowData['id']);
                    $(td).attr('class', 'editable');
                }
            },
            {
                "targets": 3,
                createdCell: function(td, cellData, rowData, row, col) {
                    $(td).attr('data-name', 'price');
                    $(td).attr('data-id', rowData['id']);
                    $(td).attr('class', 'editable');
                }
            },
            {
                "targets": 4,
                createdCell: function(td, cellData, rowData, row, col) {
                    $(td).attr('data-name', 'description');
                    $(td).attr('data-id', rowData['id']);
                    $(td).attr('class', 'editable');
                }
            },
            {
                "targets": 5,
                createdCell: function(td, cellData, rowData, row, col) {
                    $(td).attr('data-name', 'category');
                    $(td).attr('data-id', rowData['id']);
                    $(td).attr('class', 'editable');
                }
            },
            {
                "targets": 6,
                createdCell: function(td, cellData, rowData, row, col) {
                    $(td).attr('data-name', 'store');
                    $(td).attr('data-id', rowData['id']);
                    $(td).attr('class', 'editable');
                }
            },
            {
                "targets": 7,
                createdCell: function(td, cellData, rowData, row, col) {
                    $(td).attr('data-name', 'availability');
                    $(td).attr('data-id', rowData['id']);
                    $(td).attr('class', 'editable');
                }
            },
        ]
    });
});