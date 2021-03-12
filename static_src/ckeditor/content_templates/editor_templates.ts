import ImageAndTitleHtml from "./templates/image_and_title.template.html";
import SectionWelcome from "./templates/section_welcome.template.html";

console.log("im loaded")
CKEDITOR.addTemplates("default",
    {
        imagesPath: "/static/ckeditor/content_templates/images/",
        templates:[
            {
                title:"Index welcome section",
                image:"template1.gif",
                description:"Welcome section content",
                html: SectionWelcome,
            },
            // {
            //     title:"Image and Title",
            //     image:"template1.gif",
            //     description:"One main image with a title and text that surround the image.",
            //     html: ImageAndTitleHtml,
            // },

        ]
    }
);
