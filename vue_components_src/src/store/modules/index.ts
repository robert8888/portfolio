export {default as menu} from "@/store/modules/menu";
export {default as card} from "@/store/modules/card";
export {default as projects} from "@/store/modules/projects";
export {default as cv} from "@/store/modules/cv";

import {
    MUTATIONS as MENU_MUTATION,
    ACTIONS as MENU_ACTIONS,
    GETTERS as MENU_GETTERS,
} from "@/store/modules/menu";

import {
    MUTATIONS as CARD_MUTATION,
    ACTIONS as CARD_ACTIONS,
    GETTERS as CARD_GETTERS,
} from "@/store/modules/card";

import {
    MUTATIONS as PROJECTS_MUTATION,
    ACTIONS as PROJECTS_ACTIONS,
    GETTERS as PROJECTS_GETTERS,
} from "@/store/modules/projects"

import {
    MUTATIONS as CV_MUTATIONS,
    ACTIONS as CV_ACTIONS,
    GETTERS as CV_GETTERS,
} from "@/store/modules/cv";


export const MUTATIONS = {
    ...MENU_MUTATION,
    ...CARD_MUTATION,
    ...PROJECTS_MUTATION,
    ...CV_MUTATIONS
}

export const ACTIONS = {
    ...MENU_ACTIONS,
    ...CARD_ACTIONS,
    ...PROJECTS_ACTIONS,
    ...CV_ACTIONS
}

export const GETTERS = {
    ...MENU_GETTERS,
    ...CARD_GETTERS,
    ...PROJECTS_GETTERS,
    ...CV_GETTERS
}