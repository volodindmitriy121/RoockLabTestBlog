$('document').ready(function () {

    let loadForm = function () {
        let btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-board .modal-content").html("");
                $("#modal-board").modal("show");
            },
            success: function (data) {
                $("#modal-board .modal-content").html(data.html_form);
            }
        });
    };

    let saveForm = function () {
        let form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#board-table tbody").html(data.html_board_list);
                    $("#modal-board").modal("hide");
                }
                else {
                    $("#modal-board .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    let addBoard = function () {
        let form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#board-table tbody").append(data.html_board_list);
                    $("#modal-board").modal("hide");
                }
                else {
                    $("#modal-board .modal-content").html(data.html_form);
                }
            }

        });
        return false;
    };

        let updateBoard = function () {
        let form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#board-table tbody  ").html(data.html_board_list);
                    $("#modal-board").modal("hide");
                }
                else {
                    $("#modal-board .modal-content").html(data.html_form);
                }
            }

        });
        return false;
    };


    $(".js-create-board").click(loadForm);
    $("#modal-board").on("submit", ".js-board-create-form", saveForm);

    // Update board
    $("#board-table").on("click", ".js-update-board", loadForm);
    $("#modal-board").on("submit", ".js-board-update-form", saveForm);

    $('#board-table').on('click', '.js-delete-board', loadForm);
    $('#modal-board').on('submit', '.js-board-delete-form', saveForm);


});