
import storePlugin from "./store"

import ResizeObserver from "@/directives/ResizeObserver";

import MenuMain from "@/components/MenuMain.vue";
import MenuMainItem from "@/components/MenuMainItem.vue";
import MenuAside from "@/components/MenuAside.vue";
import MenuAsideItem from "@/components/MenuAsideItem.vue";
import Overlay from "@/components/Overlay.vue";
import Slider from "@/components/Slider.vue"
import SliderItem from "@/components/SliderItem.vue";
import CardProject from "@/components/Card.vue"
import Gallery from "@/components/Gallery.vue";
import GalleryItem from "@/components/GalleryItem.vue";
import ContactForm from "@/components/ContactForm.vue";
import FormLabel from "@/components/FormLabel.vue";
import InputCheckbox from "@/components/InputCheckbox.vue";
import ContactNumber from "@/components/ContactNumber.vue";

import CvDownloader from "@/components/CvDownloader.vue";
import CvConfigurator from "@/components/CvConfigurator.vue";
import CvConfiguratorTemplate from "@/components/CvConfiguratorTemplate.vue";
import CvConfiguratorColor from "@/components/CvConfiguratorColor.vue";


import defineVueComponent from "@/define-vue-component";

defineVueComponent(
    {
        MenuMain,
        MenuMainItem,
        MenuAside,
        MenuAsideItem,
        Overlay,
        Slider,
        SliderItem,
        CardProject,
        Gallery,
        GalleryItem,
        ContactForm,
        FormLabel,
        InputCheckbox,
        ContactNumber,

        CvDownloader,

        CvConfigurator,
        CvConfiguratorTemplate,
        CvConfiguratorColor
    }, [
        storePlugin,
        ResizeObserver,
    ]
)