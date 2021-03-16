const components = [
    'vue-component',
    'contact-form',
    'contact-form-label',
    'input',
    'textarea',
]

CKEDITOR.on( 'instanceReady', function( ev ) {
    components.forEach(compoenent => {
        ev.editor.dataProcessor.writer.setRules( compoenent, {
            indent: true,
            breakBeforeOpen: true,
            breakAfterOpen: false,
            breakBeforeClose: true,
            breakAfterClose: false
        })
    })
});
