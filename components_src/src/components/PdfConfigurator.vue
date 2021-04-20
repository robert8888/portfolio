<template>
  <div class="pdf-configurator">
    <div class="pdf-configurator__colors">
      <slider :fixed-slide-width="300">
        <slot name="colors"/>
      </slider>
    </div>
    <div class="pdf-configurator__tpls">
      <div :style="profileSchemaPropertyStyle">
        <slider :fixed-slide-width="300">
          <slot/>
        </slider>
      </div>
    </div>
  </div>
  <div class="pdf-configurator__btn-container">
    <button class="pdf-configurator__btn">{{downloadLabel}}</button>
  </div>
</template>
<script lang="ts">
import {defineComponent, computed} from "vue";
import Slider from "@/components/SimpleSlider.vue";
import {useStore, GETTERS} from "@/store";

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
    return {
      colors
    }
  },

  computed:{
    profileSchemaPropertyStyle(): Record<string, string>{
      if(!this.colors) return {};

      return Object.fromEntries(Object.entries(this.colors).map(([colorName, colorValue]: [string, string]) =>{
        return ["--" + colorName.split(/(?=[A-Z])/).map(name => name.toLowerCase()).join("-"), colorValue]
      }))
    }
  }
})
</script>