<template>
  <div class="projects__search"
       role="combobox"
       :aria-owns="'autocomplete-results-'+id"
       aria-haspopup="listbox"
       :aria-expanded="autocompleteVisible">
    <input ref="input"
           type="text"
           class="projects__search-input"
           autocomplete="off"
           :aria-label="label"
           :aria-activedescendant="activedescendant"
           aria-autocomplete="both"
           :aria-controls="'autocomplete-results-'+id"
           role="searchbox"
           :placeholder="label"
           v-model="value"
           @input="onInput"
           @focus="onFocus"
           @keydown.enter="onEnter"
           @keydown.down.up="changeHintSelection"
           @keydown.space="onSpace"
           @cut="onClipboard"
           @paste="onClipboard">
    <button class="projects__search-button" @click="onButtonClick" aria-label="search"/>
    <ul :class="['projects__search__list', {'projects__search__list--visible': autocompleteVisible}]"
        :id="'autocomplete-results-'+id"
        role="listbox"
        @mouseleave="onAutocompleteListLeve">
      <li :class="['projects__search__item', {'projects__search__item--selected': index === selectedHintIndex}]"
          role="value"
          :aria-selected="index === selectedHintIndex"
          @mouseenter="onHintEnter"
          @click="onHintClick"
          v-for="(hint, index) in hintList"
          :key="hint"
          v-html="hint"
          :id="id + '-hint-item-' + index"
      >
      </li>
    </ul>
  </div>
</template>
<script lang="ts">
import {computed, defineComponent} from "vue";
import {ACTIONS, GETTERS, useStore} from "@/store";
import getUrlParam from "@/utils/get-url-param";
import {debounce} from "ts-debounce";
import toRange from "@/utils/to-range";
import nanoid from "@/utils/nano-id-html";
import setUrlParam from "@/utils/set-url-param";

interface ComponentState{
  id: string;
  value: string;
  storedValue: string;
  acceptedValue: string;
  autocompleteVisible: boolean;
  selectedHintIndex: number;
  searchHistory: string[];
  activedescendant: string | null;
}

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

  data(): ComponentState{
    return {
      id: nanoid(),
      value: "",
      storedValue: "",
      acceptedValue: "",
      autocompleteVisible: false,
      selectedHintIndex: -1,
      searchHistory: new Array<string>(),
      activedescendant: null,
    }
  },

  mounted(){
    if(this.initValue){
      this.value = this.initValue;
      this.acceptedValue = this.initValue;
    }
    window.addEventListener('click', this.onWindowClick)
  },

  unmounted() {
    window.removeEventListener('click', this.onWindowClick);
  },

  setup(props){
     const store = useStore();
     const initValue = decodeURI(getUrlParam(props.param)[0] || '');

     const fireSearch = (value: string) => {
       store.dispatch(ACTIONS.UPDATE_FILTER, {type: props.param, value})
     }
     const updateAutoComplete = debounce((input: string) => {
       store.dispatch(ACTIONS.UPDATE_AUTOCOMPLETE, input)
     }, 100)

     const hintList = computed(() => store.getters[GETTERS.GET_AUTOCOMPLETE] as string[])

     return { fireSearch, updateAutoComplete, initValue, hintList }
  },

  computed:{
    autocompleteValue(): string{
      return this.value.substring(this.acceptedValue.length);
    },

    lastWord(): string{
      return this.value.split(' ')?.pop()?.trim() || this.value.trim();
    }
  },

  methods: {
    onInput: function(){
        this.updateAutocomplete();
    },

    onFocus(){
      this.updateAutocomplete();
    },

    onButtonClick(){
      this.startSearching();
    },

    onEnter(){
      if(this.selectedHintIndex < 0){
        this.startSearching();
      } else {
        this.closeAutocomplete();
      }
    },

    onSpace(){
      if(this.hintList
          .map((hint: string) => hint.replace(/<.*?>/g, ''))
          .find((hint: string) => hint.indexOf(this.lastWord)))
      {
        this.setCurrentAsAccepted();
      }
    },

    onClipboard(){
      setTimeout(() => this.setCurrentAsAccepted(), 16)
    },

    startSearching(){
      this.fireSearch(this.value)
      this.setCurrentAsAccepted();
      this.searchHistory.push(this.value);
      setUrlParam(this.param, this.value)
    },

    updateAutocomplete(){
      const autoCompleteValue = this.autocompleteValue;
      if(autoCompleteValue)
        this.updateAutoComplete(this.autocompleteValue);
    },

    changeHintSelection(e: KeyboardEvent){
      e.preventDefault();
      const delta = (e.key === "ArrowDown") ? 1 : -1;
      if(!this.autocompleteVisible){
        const index = this.searchHistory.indexOf(this.value);
        const newIndex = toRange(index + delta, 0, this.searchHistory.length - 1);
        this.value = this.searchHistory[newIndex];
        this.setCurrentAsAccepted();
        return;
      }
      this.selectedHintIndex = toRange(
         this.selectedHintIndex + delta,
         -1, this.hintList.length - 1
      );
    },

    setHintAsPlaceholder(){
      const hint = this.hintList[this.selectedHintIndex];
      let replacement = ""
      if(hint.startsWith('<b>')){
        replacement = hint;
      } else {
        const start = hint.indexOf("<b>");
        const end = hint.lastIndexOf("</b>");
        replacement = hint.substring(start, end);
      }
      replacement = replacement.replace(/<.*?>/g, "").trim();
      const prefix = this.acceptedValue ? this.acceptedValue + " " : ""
      this.value = prefix + replacement;
    },

    closeAutocomplete(){
      this.autocompleteVisible = false;
      if(this.selectedHintIndex >= 0){
        this.storedValue = this.value;
        this.acceptedValue = this.value;
        this.selectedHintIndex = -1;
      }
    },

    setCurrentAsAccepted(){
      this.acceptedValue = this.value
    },

    onWindowClick(e: Event){
      const target = e.target as HTMLElement;
      if(!target.closest('.projects__search'))
        this.autocompleteVisible = false;
    },

    // hint mouse events ----------------

    getElementIndex(el: HTMLElement){
      const parent = el.parentNode;
      if(!parent)
        return -1;
      return [...parent.children].indexOf(el)
    },

    setElementAsCurrent(el: HTMLElement){
      const index = this.getElementIndex(el);
      this.selectedHintIndex = index;
    },

    onHintEnter(event: MouseEvent){
      this.setElementAsCurrent(event.target as HTMLElement);
    },

    onHintClick(event: MouseEvent){
      this.setElementAsCurrent(event.target as HTMLElement);
      this.closeAutocomplete();
    },

    onAutocompleteListLeve(){
      this.selectedHintIndex = -1;
    },

    setActivedescendant(index: number){
      if(index < 0)
        return this.activedescendant = null

      this.activedescendant = this.id + '-hint-item-'+ index;
    }
  },

  watch:{
    hintList:{
      deep: true,
      handler(){
        this.autocompleteVisible = true
      }
    },
    selectedHintIndex(newIndex: number, oldIndex: number) {
      if(newIndex >= 0 && oldIndex === -1){
        this.storedValue = this.value

      } else if(newIndex === -1 && oldIndex >= 0) {
        this.value = this.storedValue;
      }

      this.setActivedescendant(newIndex);

      if(newIndex < 0)
        return;

      this.setHintAsPlaceholder()
    },
    value(newValue, oldValue){
      if(newValue.length < oldValue.length &&
         newValue.length < this.acceptedValue.length)
      {
        if(this.value.endsWith(' ')){
          this.setCurrentAsAccepted();
          return
        }
        const newAccepted = this.value.split(" ");
        newAccepted.pop();
        this.acceptedValue = newAccepted.join(" ");
      }
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