const components = [
    'vue-component',
    'contact-form',
    'contact-form-label',
    'input',
    'textarea',
]


interface Window {
    CKEDITOR: CKEDITOR;
}

if(window.CKEDITOR){
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
}
