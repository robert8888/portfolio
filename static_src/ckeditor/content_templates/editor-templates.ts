import ImageAndTitleHtml from "./templates/image_and_title.template.html";
import SectionWelcome from "./templates/section_welcome.template.html";
import SectionAbout from "./templates/section_about.template.html";
import SectionContactForm from "./templates/section_contact-form.template.html";

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
            {
                title:"Index about section",
                image:"template1.gif",
                description:"About section content with photo",
                html: SectionAbout,
            },
            {
                title:"Index contact section",
                image:"template1.gif",
                description:"Contact section Form",
                html: SectionContactForm,
            },
        ]
    }
);
