
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
import ContactFormLabel from "@/components/ContactFormLabel.vue";
import ContactNumber from "@/components/ContactNumber.vue";
import PdfPreloader from "@/components/PdfPreloader.vue";
import PdfConfigurator from "@/components/PdfConfigurator.vue";
import PdfConfiguratorTemplate from "@/components/PdfConfiguratorTemplate.vue";
import PdfConfiguratorColor from "@/components/PdfConfiguratorColor.vue";

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
        ContactFormLabel,
        ContactNumber,
        PdfPreloader,
        PdfConfigurator,
        PdfConfiguratorTemplate,
        PdfConfiguratorColor
    }, [
        storePlugin,
        ResizeObserver,
    ]
)