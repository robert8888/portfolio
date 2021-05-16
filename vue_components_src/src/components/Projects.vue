<template>
  <div class="projects">
    <div v-if="showInitialRenderedContent" :class="['projects__container', {'projects__container--loading': status.loading}]">
      <slot/>
    </div>
    <template v-else>
      <div :class="['projects__container', {'projects__container--loading': status.loading}]">
        <card-project v-for="project in projects"
                      :key="project.title"
                      :id="project.slug"
                      :href="project.path"
                      :more-text="project.moreText">
          <template #header>
            <a class="card-project__title-link" :href="project.path" v-html="project.title"></a>
            <a class="card-project__type-link" :href="currentPath + '?type=' + project.typeValue"> {{project.type}}</a>
          </template>
          <template #gallery>
            <gallery>
              <gallery-item v-for="image in project.images" :key="image.url.slice(-10)" :thumb-src="image.url"></gallery-item>
            </gallery>
          </template>
          <h4 class="card-project__subtitle">
            <a :href="project.path" v-html="project.subtitle"/>
          </h4>
          <div class="card-project__text" v-html="project.description"></div>
          <ul class="card-project__tech-list">
            <li v-for="tech in project.technologies" :key="tech.name"
                :class="['card-project__tech-list-item', {'card-project__tech-list-item--highlighted': tech.isHighlighted}] "
                :style="{'--color': tech.color}">
              <a class="card-project__tech-list-link js" :href="tech.link">
                {{tech.name}}
              </a>
            </li>
          </ul>
        </card-project>
      </div>
    </template>
    <div class="projects__loading-container" ref="loading" :style="[status.fetching ? {display: 'grid'} : {display: 'none'}]">
      <div class="card-project--demo"/>
      <div class="card-project--demo"/>
      <div class="card-project--demo"/>
      <div class="card-project--demo"/>
    </div>
  </div>
</template>
<script lang="ts">
import {computed, defineComponent, watch } from "vue";
import Spinner from "@/components/Spinner.vue";
import {ACTIONS, useStore} from "@/store";
import CardProject from "@/components/Card.vue";
import Gallery from "@/components/Gallery.vue";
import GalleryItem from "@/components/GalleryItem.vue";

export default defineComponent({
  components: {Spinner, CardProject, Gallery, GalleryItem},

  data(){
    return {
      showInitialRenderedContent: true,
      currentPath: location.pathname
    }
  },

  setup(){
    const store = useStore();
    const filters = computed(() => store.state.projects.filter)
    const order = computed(() => store.state.projects.order)
    const status = computed(() => store.state.projects.status)
    const projects  = computed(() => store.state.projects.projects)

    const setupTime = performance.now()
    watch([filters,  order], () =>{
      if(performance.now() - setupTime < 300)
          return
      store.dispatch(ACTIONS.FETCH_PROJECTS)
    }, {deep: true})
    return {
      status,
      projects,
    }
  },

  //
  watch:{
    projects(){
      if(this.showInitialRenderedContent)
        this.showInitialRenderedContent = false;
    }
  }
})
</script>
