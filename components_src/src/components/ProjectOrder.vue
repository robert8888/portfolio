<template>
  <select-component
      :label="label"
      @onChange="filterChange"
      :selected="selected"
      mode="single">
    <slot/>
  </select-component>
</template>
<script lang="ts">
import {defineComponent} from "vue";
import {useStore, ACTIONS} from "@/store";
import SelectItem from "@/components/SelectItem.vue";
import SelectComponent from "@/components/Select.vue"
import getUrlParam from "@/utils/get-url-param";
import setUrlParam from "@/utils/set-url-param";

export default defineComponent({
  components: {SelectComponent, SelectItem},

  props: {
    label: {
      type: String,
      require: true,
    },
    param: {
      type: String,
      require: true,
      default: '',
    }
  },

  setup(props){
    const store = useStore();
    const selected = getUrlParam(props.param);

    const update = (value: string) => {
      store.dispatch(ACTIONS.UPDATE_ORDER, { value, param: props.param })
    }
    return {selected, update }
  },

  methods: {
    filterChange({values}: {values: string[]}){
       this.update(values[0]);
       setUrlParam(this.param, values);
    }
  }
})
</script>