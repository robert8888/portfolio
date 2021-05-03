<template>
  <aside class="navigation navigation--aside" >
    <nav class="navigation__container" >
      <div class="navigation__item navigation__home">
        <a href="/" class="navigation__item__link">
          <span class="navigation__item__content">#</span>
        </a>
      </div>
      <list class="navigation__list" ref="list">
        <slot/>
      </list>
      <div class="navigation__item navigation__fast-scroll">
        <button @click="fastScroll"
                :class="fastScrollButtonClass"
                :aria-label="'scroll ' + fastScrollDir"/>
      </div>
    </nav>
    <div class="navigation__progress">
      <transition appear :duration="1400" name="block-thumb">
        <div class="navigation__progress__thumb" :style="thumbStyle"/>
      </transition>
    </div>
  </aside>
</template>
<script lang="ts">
import {defineComponent, computed, nextTick} from "vue";
import List from "./List.vue";
import getWindowScrollHeight from "@/utils/window-scroll-height";
import {debounce} from "ts-debounce";
import {getUrlAnchor, setUrlAnchor} from "@/utils/url-anchor";

interface MenuAsideData{
  currentIntersectedIndex: number | undefined;
  intersectionObserver: IntersectionObserver | undefined;
  resizeObserver: ResizeObserver | undefined;
  targetsToIndex: WeakMap<Element, number>;
  indexToTargets: Map<number, Element>;
  indexToSelector: Map<number, string>;
  selectorToIndex: Map<string, number>;
  length: number;
  thumbTopPosition: number;
}

export default defineComponent({
  components: {List},

  props: {
     excludeFirst: {
       type: Boolean,
       default: true,
     }
  },

  data(): MenuAsideData{
    return{
      currentIntersectedIndex: -1,
      intersectionObserver: undefined,
      resizeObserver: undefined,
      targetsToIndex: new WeakMap<Element, number>(),
      indexToTargets: new Map<number, Element>(),
      indexToSelector: new Map<number, string>(),
      selectorToIndex: new Map<string, number>(),
      length: 0,
      thumbTopPosition: 0
    }
  },

  created() {
    this.intersectionObserver = new IntersectionObserver(this.intersect, {
      rootMargin: "-49% 0px -49% 0px"
    })

    this.resizeObserver = new ResizeObserver(debounce(this.updateThumbPosition.bind(this), 50))
  },

  mounted(): void {
    this.length = this.listRef().children.length;
    this.resizeObserver?.observe(document.body);
    this.scrollToStartPosition();
  },

  unmounted() {
    this.intersectionObserver?.disconnect();
    this.resizeObserver?.disconnect();
  },

  computed:{
     fastScrollDir(): string{
       return (this.currentIntersectedIndex || 0) < this.length - 1 ?  "down" : "up"
     },

     fastScrollButtonClass(): string{
       return `navigation__fast-scroll__btn navigation__fast-scroll__btn--${this.fastScrollDir}`
     },

     thumbStyle(): string{
        return `transform: translateY(${this.thumbTopPosition}px)`
     }
  },

  provide(){
    return {
      registerObservable: (index: number, selector: string) => {
        if(!selector)
          return;
        const target = document.querySelector(selector);
        if(!target || !this.intersectionObserver)
          return;
        this.targetsToIndex.set(target, index);
        this.indexToTargets.set(index, target);
        this.indexToSelector.set(index, selector);
        this.selectorToIndex.set(selector, index);
        this.intersectionObserver.observe(target)
      },
      intersected: computed(() => this.currentIntersectedIndex)
    }
  },


  methods:{
    listRef(): HTMLElement{
      //@ts-ignore
      return this.$refs?.list?.$el;
    },

    intersect(entries: IntersectionObserverEntry[]): void{
      const intersecting = entries.find(entry => entry.isIntersecting);
      if(!intersecting) return
      this.currentIntersectedIndex = this.targetsToIndex.get(intersecting.target);
      nextTick(() => this.updateThumbPosition());
    },

    updateThumbPosition(){
      const index = this.currentIntersectedIndex || 0
      const currentSelectedItem = this.listRef()?.children[index - 1];
      if(!currentSelectedItem) return;
      this.thumbTopPosition = currentSelectedItem.getBoundingClientRect().top;
    },

    fastScroll(){
      const position = this.fastScrollDir === "down"
        ? getWindowScrollHeight() - window.innerHeight
        : 0;
      window.scrollTo({
        left: 0,
        top: position,
        behavior: "smooth"
      })
    },

    scrollToStartPosition(){
      const anchor = getUrlAnchor();
      const valid = this.selectorToIndex.has(anchor) && this.selectorToIndex.get(anchor) as number > 1;
      if(!valid)
        return;

      const target = document.querySelector(anchor);
      if(!target)
        return;

      // to prevent animations on page load
      document.body.setAttribute("data-init-anchor-scroll", "true");

      setTimeout(() => {
        target.scrollIntoView(true);
      },600)

    }
  },

  watch: {
    currentIntersectedIndex(newIndex: number, prevIndex: number){
      setUrlAnchor(this.indexToSelector.get(this.currentIntersectedIndex || 0) || "")
      this.indexToTargets.get(newIndex)?.setAttribute('data-intersecting', "true")
      this.indexToTargets.get(prevIndex)?.removeAttribute('data-intersecting')
      this.indexToTargets.get(newIndex)?.setAttribute('data-was-intersected', "true")
    }
  }
})
</script>
<style lang="scss">
.block-thumb-enter-active{
  opacity: 0;
  transform: translate(0) !important;
}

</style>
