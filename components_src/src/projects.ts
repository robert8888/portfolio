import storePlugin from "./store"

import ResizeObserver from "@/directives/ResizeObserver";

import {
    MenuMain,
    MenuMainItem,
    SelectComponent,
    SelectItem
} from "@/components";


import defineVueComponent from "@/define-vue-component";

defineVueComponent(
    {
        MenuMain,
        MenuMainItem,
        SelectComponent,
        SelectItem
    }, [
        storePlugin,
        ResizeObserver,
    ]
)
