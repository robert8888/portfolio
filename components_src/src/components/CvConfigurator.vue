<template>
  <div class="cv-configurator">
    <div class="cv-configurator__colors">
      <slider :fixed-slide-width="300" id="cv-color-slider">
        <slot name="colors"/>
      </slider>
    </div>
    <div class="cv-configurator__tpls">
      <div :style="profileSchemaPropertyStyle">
        <slider :fixed-slide-width="300" id="cv-template-slider">
          <slot/>
        </slider>
      </div>
    </div>
  </div>
  <div class="cv-configurator__btn-container">
    <button class="cv-configurator__btn" @click="confirm">{{downloadLabel}}</button>
  </div>
</template>
<script lang="ts">
import {defineComponent, computed} from "vue";
import Slider from "@/components/SimpleSlider.vue";
import {useStore, GETTERS, ACTIONS} from "@/store";

export default defineComponent({
  components: {Slider},
  props: {
    downloadLabel:{
      type: String,
      default: 'Download'
    }
  },

  setup(){
    const store = useStore()
    const colors = computed(() => store.getters[GETTERS.GET_CV_COLOR_PROFILE_COLORS] as Record<string, string>)
    const confirm = () => {
      store.dispatch(ACTIONS.CONFIRM_TEMPLATE_CONFIG)
    };
    return {
      colors,
      confirm
    }
  },

  computed:{
    profileSchemaPropertyStyle(): Record<string, string>{
      if(!this.colors) return {};
      //transforming camel case to kebab case
      return Object.fromEntries(Object.entries(this.colors).map(([colorName, colorValue]: [string, string]) =>{
        return ["--" + colorName.split(/(?=[A-Z])/).map(name => name.toLowerCase()).join("-"), colorValue]
      }))
    }
  },
})
</script>