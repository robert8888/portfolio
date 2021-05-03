<template>
  <li :id="id"
      ref="container"
      :class="['dropdown__item', {'dropdown__item--active': currentActiveId === id}]"
      role="option"
      @click="clickHandle"
      :aria-selected="isCurrentSelected">
    <slot/>
  </li>
</template>
<script lang="ts">
import {defineComponent, inject} from "vue";
import nanoid from "@/utils/nano-id-html";


export interface Item{
  id: string;
  value: string;
  text: string;
}

export default defineComponent({
  props: {
      value: {
        type: String,
        required: true,
      },
      default:{
        default: Boolean,
      },
      index: {
        type: Number,
        required: true,
      },
  },

  data(){
    return{
      id: nanoid(),
    }
  },

  setup(){
    return{
      onSelect: inject('onSelect') as (index: number) => void,
      currentSelectedIds: inject('currentSelectedIds') as string[],
      currentActiveId: inject('currentActiveId') as string,
      registerItem: inject('registerItem') as (index: number, item: Item) => void
    }
  },

  mounted() {
    this.registerItem(
      this.index, {
        id: this.id,
        value: this.value,
        text: (this.$refs.container as HTMLElement).innerHTML
      })
  },

  computed: {
    isCurrentSelected: function (): boolean{
      return this.currentSelectedIds.includes(this.id);
    }
  },

  methods: {
    clickHandle(){
      this.onSelect(this.index)
    }
  },

})
</script>