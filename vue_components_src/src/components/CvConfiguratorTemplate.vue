<template>
  <div :class="['cv-configurator__tpl', {'cv-configurator__tpl--current': templateId === currentId}]"
       @touchstart.passive="setAsCurrent"
       @click="setAsCurrent"
       @focus.prevent="setAsCurrent" 
       tabindex="0">
    <div class="cv-configurator__tpl-wrapper">
      <slot/>
      <h5>{{name}}</h5>
    </div>
  </div>
</template>
<script lang="ts">
import {computed, defineComponent} from "vue";
import {GETTERS, MUTATIONS, useStore} from "@/store";
export default defineComponent({
  props: {
    name:{
      type: String,
      required: true,
    },
    templateId:{
      type: String,
      required: true,
    }
  },


  setup(props){
    const store = useStore();
    const currentId = computed(() => store.getters[GETTERS.GET_CV_TEMPLATE_ID]);
    const setAsCurrent = () => {
      store.commit(MUTATIONS.SET_CV_TEMPLATE_ID, {
        id: props.templateId,
      })
    }
    return {
      currentId,
      setAsCurrent,
    }
  },


})
</script>