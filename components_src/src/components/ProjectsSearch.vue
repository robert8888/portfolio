<template>
  <div class="projects__search">
    <input type="text"
           class="projects__search-input"
           :aria-label="label"
           :placeholder="label"
           v-model.trim="value"
           @keydown.enter="updateValue" >
    <button class="projects__search-button"
            @click="updateValue"/>
  </div>
</template>
<script lang="ts">
import {defineComponent} from "vue";
import {ACTIONS, useStore} from "@/store";
export default defineComponent({
  props: {
    label: {
      type: String,
      default: "Search"
    },
    param: {
      type: String,
      default: "search",
      require: 'search'
    }
  },

  data(){
    return {
      value: ""
    }
  },

  setup(props){
     const store = useStore();
     const update = (value: string) => {
       store.dispatch(ACTIONS.UPDATE_FILTER, {type: props.param, value})
     }
     return { update }
  },

  methods: {
    updateValue: function (){
      this.update(this.value)
    }
  }
})
</script>