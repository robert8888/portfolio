import storePlugin from "./store"

import ResizeObserver from "@/directives/ResizeObserver";

import MenuMain from "@/components/MenuMain.vue";
import MenuMainItem from "@/components/MenuMainItem.vue";
import ProjectsFilter from "@/components/ProjectsFilter.vue";
import ProjectsOrder from "@/components/ProjectOrder.vue";
import ProjectsSearch from "@/components/ProjectsSearch.vue";
import SelectItem from "@/components/SelectItem.vue";
import SelectComponent from "@/components/Select.vue";
import Projects from "@/components/Projects.vue";
import CardProject from "@/components/Card.vue";
import Gallery from "@/components/Gallery.vue";
import GalleryItem from "@/components/GalleryItem.vue";

import defineVueComponent from "@/define-vue-component";

defineVueComponent(
    {
        MenuMain,
        MenuMainItem,
        ProjectsFilter,
        ProjectsOrder,
        ProjectsSearch,
        SelectItem,
        SelectComponent,
        Projects,
        CardProject,
        Gallery,
        GalleryItem
    }, [
        storePlugin,
        ResizeObserver,
    ]
)
