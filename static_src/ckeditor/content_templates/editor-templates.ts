import SectionWelcome from "./templates/section_welcome.template.html";
import SectionAbout from "./templates/section_about.template.html";
import SectionContactForm from "./templates/section_contact-form.template.html";
import SectionContactDescription from "./templates/section_contact-description.template.html";
import ProjectShortDescription from "./templates/project_short-description.template.html"
import ProjectFullDescription from "./templates/project_full-description.template.html"

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
                description:"Contact section form",
                html: SectionContactForm,
            },
            {
                title:"Index contact section",
                image:"template1.gif",
                description:"Contact section description",
                html: SectionContactDescription,
            },
            {
                title:"Project",
                image:"template1.gif",
                description:"Project short description",
                html: ProjectShortDescription,
            },
            {
                title:"Project",
                image:"template1.gif",
                description:"Projects full description",
                html: ProjectFullDescription,
            },
        ]
    }
);
