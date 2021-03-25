<template>
  <div class="projects__search">
    <input ref="input"
           type="text"
           class="projects__search-input"
           autocomplete="off"
           :aria-label="label"
           :placeholder="label"
           @input="onInput"
           @cut="rebuildTokens"
           @paste="rebuildTokens"
           @keydown.enter="updateValue"
           @keydown.down.up="changeSelection"
    >
    <button class="projects__search-button"
            @click="updateValue"/>
    <ul :class="['projects__search__list', {'projects__search__list--visible': autocompleteVisible}]">
      <li :class="['projects__search__item', {'projects__search__item--selected': index === currentSelected}]"
          @mouseenter="hintMouseEnter"
          @click="chooseHint"
          v-for="(hint, index) in hintList"
          :key="hint"
          v-html="hint"></li>
    </ul>
  </div>
</template>
<script lang="ts">
import {computed, defineComponent, nextTick} from "vue";
import {ACTIONS, GETTERS, useStore} from "@/store";
import getUrlParam from "@/utils/get-url-param";
import setUrlParam from "@/utils/set-url-param";
import {debounce} from "ts-debounce";
import toRange from "@/utils/to-range";

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
      value: "",
      baseTokens: new Array<string>(),
      storedValue: "",
      currentSelected: -1,
      autocompleteVisible: false,
    }
  },

  mounted(){
    if(this.search){
      (this.$refs.input as HTMLInputElement).value = this.search
      this.rebuildTokens()
    }
  },

  setup(props){
     const store = useStore();
     const search = decodeURI(getUrlParam(props.param)[0] || '');

     const update = (value: string) => {
       store.dispatch(ACTIONS.UPDATE_FILTER, {type: props.param, value})
     }
     const updateAutoComplete = debounce((input: string) => {
       store.dispatch(ACTIONS.UPDATE_AUTOCOMPLETE, input)
     }, 100)

     const hintList = computed(() => store.getters[GETTERS.GET_AUTOCOMPLETE] as string[])

     return { update, updateAutoComplete, search, hintList }
  },

  methods: {
    baseLength(): number{
      return this.baseTokens.join(' ').length;
    },

    getLastWord(value: string): string{
      return value.split(" ")?.pop()?.trim() || value.trim()
    },

    rebuildTokens(){
      console.log("rebuild tokens")
      setTimeout(() => {
        const value = (this.$refs.input as HTMLInputElement).value
        this.baseTokens = value.split(" ").filter(token => token !== " " && token !== "")
      }, 16)

    },

    chooseHint(){
      this.autocompleteVisible = false
      this.baseTokens.push(this.getLastWord(this.value))
      this.storedValue = this.value + " ";
    },

    updateValue: function (){
      if(this.currentSelected < 0 || !this.autocompleteVisible){
        this.update(this.value)
        setUrlParam(this.param, this.value ? this.value : [])
      } else {
        this.chooseHint()
        // this.updateValueFromHint(this.value.substring(this.baseValue.length), this.hintList[this.currentSelected])
      }
    },


    onInput: function(){
      const newValue = (this.$refs.input as HTMLInputElement).value
      if(newValue.length < this.value.length)
        this.rebuildTokens()
      this.value = newValue;
      const lastWord = this.getLastWord(this.value);
      console.log(lastWord)
      if(!lastWord)
        return
      this.updateAutoComplete(lastWord)
    },


    changeSelection(e: KeyboardEvent){
      const delta = (e.key === "ArrowDown") ? 1 : -1
      this.currentSelected = toRange(this.currentSelected + delta, -1, this.hintList.length - 1);
    },

    hintMouseEnter(e: MouseEvent){
      const target = (e.target as HTMLElement)
      const parent = target?.parentNode;
      if(!parent) return;
      this.currentSelected = [...parent.children].indexOf(target)
      this.storedValue = this.value
    },

    hintMouseLeve(){
      this.value = this.storedValue;
    },

    updateValueFromHint(value: string, hint: string){
      if(hint.startsWith("<b>")){
        this.value = this.baseTokens.join(' ') + ' ' + hint.replace(/<.*?>/g, '');
      } else {
        const startIndex = hint.indexOf('<b>')
        const endIndex = hint.lastIndexOf('</b>')
        const word = hint.substring(startIndex, endIndex).replace(/<.*?>/g, '');
        const words  = value.split(' ')
        words.pop()
        words.push(word)
        this.value = this.baseTokens.join(' ') + ' ' + words.join(' ')
      }
      (this.$refs.input as HTMLInputElement).value = this.value
      // (this.$refs.input as HTMLInputElement).setSelectionRange()
    }


  },

  watch:{
    hintList:{
      deep: true,
      handler(){
        this.autocompleteVisible = true
      }
    },
    currentSelected(newIndex: number, oldIndex: number) {
      if(newIndex >= 0 ){
        if(oldIndex === -1){
          this.storedValue = this.value
        }
        this.updateValueFromHint(
            this.storedValue.substring(this.baseLength()),
            this.hintList[newIndex]
        )
      } else if(newIndex === -1 && oldIndex >= 0) {
        this.value = this.storedValue;
        (this.$refs.input as HTMLInputElement).value = this.value
      }
    },

    autocompleteVisible(value){
      if(value)
        this.currentSelected = -1
    }

  }

})
</script>
<style scoped>
.projects__search{
  position: relative;
}
.projects__search-hints{
  position: absolute;
}
</style>