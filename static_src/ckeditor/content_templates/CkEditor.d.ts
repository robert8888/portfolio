
type Template = {
    image: string;
    description: string;
    html: string;
    title: string;
}

type Templates = {
    imagesPath: string;
    templates: Template[]
}

type Rule = {
    indent?: boolean;
    breakBeforeOpen?: boolean;
    breakAfterOpen?: boolean;
    breakBeforeClose?: boolean;
    breakAfterClose?: boolean;
};

interface Event{
    editor: {
        dataProcessor: {
            writer:{
                setRules(el: string, rule: Rule)
            }
        }
    }
}


declare class CKEDITOR{
    static plugins: Plugins;

    static addTemplates(name: string, templates: Templates) {

    }
    static getUrl(path: string) {
        return "";
    }

    static on(name: string, callback: (ev: Event) => void) {

    }
}