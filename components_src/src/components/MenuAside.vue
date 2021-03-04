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
        <button @click="fastScroll" :class="fastScrollButtonClass"/>
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
import getWindowScrollHeight from "@/utils/windowScrollHeight";
import {debounce} from "ts-debounce";

interface MenuAsideData{
  currentIntersectedIndex: number | undefined;
  intersectionObserver: IntersectionObserver | undefined;
  resizeObserver: ResizeObserver | undefined;
  watched: WeakMap<Element, number>;
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
      watched: new WeakMap<Element, number>(),
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
    this.resizeObserver?.observe(document.body)
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
        this.watched.set(target, index);
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
      this.currentIntersectedIndex = this.watched.get(intersecting.target);
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
    }


  },
})
</script>
<style lang="scss">
.block-thumb-enter-active{
  opacity: 0;
  transform: translate(0) !important;
}

</style>
