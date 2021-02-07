import ImageAndTitleHtml from "./templates/image_and_title.template.html";

CKEDITOR.addTemplates("default",
    {
        imagesPath: "/static/ckeditor/content_templates/images/",
        templates:[
            {
                title:"Image and Title",
                image:"template1.gif",
                description:"One main image with a title and text that surround the image.",
                html: ImageAndTitleHtml,
            }
        ]
    }
);
