$("#select_espacio").on('change', function () {
    var espacio = $(this).find(':selected').val();
    window.location.href = '/espacio/' + espacio + '/';
});