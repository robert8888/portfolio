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
import getUrlParam from "@/utils/get-url-param";
import setUrlParam from "@/utils/set-url-param";

export default defineComponent({
  props: {
    label: {
      type: String,
      default: "Search"
    },
    param: {
      type: String,
      default: "search",
      require: true
    }
  },

  data(){
    return {
      value: ""
    }
  },

  mounted(){
    if(this.search){
      this.value = this.search
    }
  },

  setup(props){
     const store = useStore();
      const search = decodeURI(getUrlParam(props.param)[0] || '');

     const update = (value: string) => {
       store.dispatch(ACTIONS.UPDATE_FILTER, {type: props.param, value})
     }
     return { update, search }
  },

  methods: {
    updateValue: function (){
      this.update(this.value)
      setUrlParam(this.param, this.value ? this.value : [])
    }
  }
})
</script>