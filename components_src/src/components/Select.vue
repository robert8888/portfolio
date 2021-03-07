<template>
  <div :id="id" :class="['dropdown', {'dropdown--multi': mode === 'multi'}]">
    <span class="dropdown__label" :id="'label-' + id">{{label}}</span>
    <div class="dropdown__list-container">
      <button type="button"
              :id="'button-'+id"
              class="dropdown__button"
              aria-haspopup="listbox"
              aria-keyshortcuts="Enter"
              :aria-expanded="isExpanded ? true : null"
              :aria-labelledby="`label-${id} button-${id}`"
              @click="buttonClick"
              @keydown="keyDown"
              v-html="buttonContent">
      </button>
      <list :class="['dropdown__list', {'dropdown__list--expanded': isExpanded}]"
          :id="'list-'+id"
          role="listbox"
          :aria-labelledby="'label-' + id"
          :aria-activedescendant="activeDescendantId"
          :aria-multiselectable="$props.mode === 'multi'"
          tabindex="-1">
        <slot/>
      </list>
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent, computed} from "vue";
import nanoid from "@/utils/nano-id-html";
import {Item} from "./SelectItem.vue";
import toRange from "@/utils/to-range";
import List from "./List.vue";
import arrayTake from "@/utils/array-take";

interface ComponentData {
  id: string;
  currentActiveIndex: number;
  currentSelectedIndexes: number[];
  items: Item[];
  isExpanded: boolean;
}

export default defineComponent({
  components: {List},

  props: {
    label: String,
    mode: {
      type: String,
      default: "single",
      validator: (value: string) =>{
        return ['single', 'multi'].includes(value)
      }
    },
    selected: {
      type: Array,
    }
  },

  emits: ['onChange'],

  data(): ComponentData{
    return {
      id: nanoid(),
      currentActiveIndex: -1,
      currentSelectedIndexes: new Array<number>(),
      items: new Array<Item>(),
      isExpanded: false,
    }
  },


  provide(){
    return {
      onSelect: (index: number) => {
        if(this.mode === "multi"){
          this.toggleSelectedIndexes(index)
        } else {
          this.setSelectedIndex(index);
          this.collapse();
        }
      },

      currentSelectedIds: computed(() =>
          this.currentSelectedItems.map(item => item.id)
      ),

      currentActiveId: computed(() =>
        this.items[this.currentActiveIndex]?.id || ""
      ),

      registerItem: (index: number, item: Item) => {
         const nextItems = [...this.items];
         nextItems[index] = item;
         this.items = nextItems;

         if(this.selected && this.selected.includes(item.value)){
           this.currentSelectedIndexes.push(index);
           this.currentActiveIndex = index;
         }
      }
    }
  },

  computed:{
     currentSelectedItems: function (): Item[]{
        return this.items.filter((item, index) => this.currentSelectedIndexes.includes(index));
     },

     activeDescendantId: function (): string | null {
       return this.currentActiveIndex !== -1
           ? this.items[this.currentActiveIndex].id
           : null;
     },
     buttonContent: function (): string{
       return this.currentSelectedIndexes.length
         ? this.currentSelectedItems.map((item: Item) => item.text).join(" - ")
         : " - "
     }
  },

  methods: {
    expand(){
      this.isExpanded = true;
      window.addEventListener("click", this.onWindowClick);
    },

    collapse(){
      this.isExpanded = false;
      window.removeEventListener("click", this.onWindowClick)
      if(this.mode === "multi"){
        this.currentActiveIndex = -1;
      }
    },

    onWindowClick(e: Event){
       if((e.target as HTMLElement).closest('#'+this.id))
         return;
      this.collapse();
    },

    buttonClick(){ this.expand(); },


    setCurrentActiveIndex(index: number){
      this.currentActiveIndex = toRange(index, 0 , this.items.length - 1)
    },

    setSelectedIndex(index: number){
      this.setCurrentActiveIndex(index);
      this.currentSelectedIndexes = [this.currentActiveIndex];
    },

    setSelectedIndexes(indexes: number[]){
      const valid = (index: number) => index >= 0 && index < this.items.length - 1;
      if(indexes.some(index => valid(index)))
        return;
      this.currentSelectedIndexes = indexes;
    },

    toggleSelectedIndexes(index: number){
      const position = this.currentSelectedIndexes.indexOf(index);
      if(position === -1){
        this.currentSelectedIndexes.push(index);
      } else {
        this.currentSelectedIndexes.splice(position, 1);
      }
    },

    keyDown(e: KeyboardEvent){
      switch (e.key){
        case "ArrowUp": {
          if(this.mode === "single"){
            this.setSelectedIndex(this.currentActiveIndex - 1)
          } else {
            this.setCurrentActiveIndex(this.currentActiveIndex - 1)
          }
          break;
        }
        case "ArrowDown": {
          if(this.mode === "single"){
            this.setSelectedIndex(this.currentActiveIndex + 1)
          } else {
            this.setCurrentActiveIndex(this.currentActiveIndex + 1)
          }
          break;
        }
        case "Enter": {
          e.preventDefault();
          if(this.mode === "single"){
             this.isExpanded
              ? this.collapse()
              : this.expand();
          } else {
            if(!this.isExpanded){
              this.expand()
            } else {
              this.toggleSelectedIndexes(this.currentActiveIndex);
            }
          }
          break;
        }
        case "Tab": {
          this.collapse();
          break;
        }
        case "Escape": {
          this.collapse();
          break;
        }
      }
    },
  },

  watch:{
    currentSelectedIndexes: {
      deep: true,
      handler: function (){
        if(!this.items.length)
          return;
        const items = arrayTake<Item>(this.items, this.currentSelectedIndexes)
        this.$emit('onChange', {
          ids: this.currentSelectedIndexes,
          values: items.map(item => item.value)
        })
      }
    }
  }
})
</script>
<style lang="scss">
.dropdown{
  display: flex;
  &__button{
    width: 100%;
  }
  &__list-container{
    position: relative;
  }
  &__list{
    list-style: none;
    display: none;
    position: absolute;
    left: 0;
    right: 0;
    &--expanded{
      display: block;
    }
  }
}
</style>