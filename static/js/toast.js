function general_toast(message_tag, message) {
    var isRtl = $('html').attr('data-textdirection') === 'rtl'
    toastr[message_tag](message, '', {
        closeButton: true,
        tapToDismiss: false,
        progressBar: true,
        rtl: isRtl
    });


}
