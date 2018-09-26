$("#select_monitor").on('change', function () {
    var monitor = $(this).find(':selected').val();
    window.location.href = '/monitor/' + monitor + '/';
});