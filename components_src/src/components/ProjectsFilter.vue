<template>
  <select-component
      :label="label"
      @onChange="filterChange"
      :selected="selected"
      mode="multi">
    <slot/>
  </select-component>
</template>
<script lang="ts">
import {computed, defineComponent} from "vue";
import {useStore, ACTIONS} from "@/store";
import SelectItem from "@/components/SelectItem.vue";
import SelectComponent from "@/components/Select.vue"
import getUrlParam from "@/utils/get-url-param";
import setUrlParam from "@/utils/set-url-param";
import shallowArrayEqual from "@/utils/shallow-array-compare";

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

    const update = (value: string[]) => {
      store.dispatch(ACTIONS.UPDATE_FILTER, {type: props.param, value})
    }

    return { selected, update}
  },

  methods: {
    filterChange({values}: {values: string[]}){
      this.update(values);
      setUrlParam(this.param, values);
    }
  },

})
</script>
