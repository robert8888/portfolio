<template>
  <li :class="className">
    <a :href="href"
       @click="linkClick"
       class="navigation__list-item__link">
      <span v-if="href" class="navigation__list-item__counter">
        {{'0' + internalIndex}}
      </span>
      <span class="navigation__list-item__content">
        <slot/>
      </span>
    </a>
  </li>
</template>
<script lang="ts">
import {defineComponent, inject} from "vue";

export default defineComponent({
  props:{
    href: {
      type: String,
    },
    class: {
      type: String
    },
    default:{
      type: Boolean,
      default: false,
    },
    index:{
      type: Number,
      required: true,
    }
  },


  setup(props){
    const registerObservable = inject("registerObservable") as (index: number, selector: string) => void;
    const currentIntersected = inject("intersected") as number;
    registerObservable(props.index + 1, props.href || "")
    return {
      currentIntersected,
      internalIndex: props.index + 1
    }
  },

  computed: {
    className(): string{
      return `navigation__item navigation__list-item` + (this.isCurrent ? ' navigation__list-item--current' : '')
    },
    isCurrent(): boolean{
       return (
           (this.internalIndex === this.currentIntersected )||
           (this.currentIntersected === -1  && this.default)
       )
    }
  },

  methods: {
    linkClick(event: MouseEvent){
      event.preventDefault();
      if(!this.href){
        window.scrollTo({
          top: 0,
          behavior: "smooth"
        })
      } else {
        const target = document.querySelector(this.href);
        if(!target)
          return;
        target.scrollIntoView({behavior: "smooth"})
      }
    }
  }
})

</script>