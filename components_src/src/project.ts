import storePlugin from "./store"

import MenuMain from "@/components/MenuMain.vue";
import MenuMainItem from "@/components/MenuMainItem.vue";
import Gallery from "@/components/Gallery.vue";
import GalleryItem from "@/components/GalleryItem.vue"


import defineVueComponent from "@/define-vue-component";

defineVueComponent(
    {
        MenuMain,
        MenuMainItem,
        Gallery,
        GalleryItem
    }, [
        storePlugin,
    ]
)
