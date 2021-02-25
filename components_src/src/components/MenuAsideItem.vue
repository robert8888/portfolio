<template>
  <li :class="className">
    <a :href="href"
       @click="linkClick"
       class="navigation__item__link">
      <span v-if="href" class="navigation__item__counter">
        {{'0' + index}}
      </span>
      <span class="navigation__item__content">
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
    defaultCurrent:{
      type: Boolean,
    },
    index:{
      type: Number,
      required: true,
    }
  },

  setup(props){
    const registerObservable = inject("registerObservable") as (index: number, selector: string) => void;
    const currentIntersected = inject("intersected") as number;
    registerObservable(props.index, props.href || "")
    return {currentIntersected}
  },

  computed: {
    className(): string{
      return `navigation__item` + (this.isCurrent ? ' navigation__item--current' : '')
    },
    isCurrent(): boolean{
       return this.index === this.currentIntersected
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