toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": true,
    "positionClass": "toast-bottom-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "1000",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "5000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"}
toastr.options.toastClass = 'toastr';

var eventSource = new EventSource("/events/")
eventSource.onmessage = function(e) {
    var json_data = JSON.parse(e.data);
    toastr[json_data.category](json_data.message, json_data.title)
};