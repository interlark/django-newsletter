// Переключение выпадающего списка при клике кнопок в нем
$(document).ready(function() {
    $(".dropdown-menu button[type='submit'].dropdown-item").click(function (e) {
        e.preventDefault();
        $(this).closest(".dropdown").find(".dropdown-toggle").dropdown('toggle');
        $(this).closest("form").submit();
    });
});
