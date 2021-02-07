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

interface Plugins{
    getPath(name: string): string;
}

declare class CKEDITOR{
    static plugins: Plugins;

    static addTemplates(name: string, templates: Templates) {

    }
    static getUrl(path: string) {
        return "";
    }
}