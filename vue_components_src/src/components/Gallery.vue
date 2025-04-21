<template>
  <div class="gallery">
     <div class="gallery__container" ref="container" v-size="updateContainerSize">
        <ul class="gallery__list" ref="list" v-on:touchstart.passive="touchStart">
          <slot/>
        </ul>
       <div class="gallery__controls">
         <button class="gallery__controls__btn"
                 @mouseup="prev"
                 :disabled="prevDisabled"
                 aria-label="previous"
                 tabindex="-1"/>
         <button class="gallery__controls__btn"
                 @mouseup="next"
                 :disabled="nextDisabled"
                 aria-label="next"
                 tabindex="-1"/>
       </div>
     </div>
  </div>
</template>

<script lang="ts">
import {computed, defineComponent, inject} from 'vue';
import toRange from "@/utils/to-range";
import {useStore, MUTATIONS, GETTERS} from "@/store";

export default defineComponent({
  data(){
    return {
      containerSize: {
        w: 0,
        h: 0,
      },
      index: 0,
      position: 0,
      isAnimated: false,
      prevDisabled: true,
      nextDisabled: false,
    }
  },

  setup(){
     const id = inject("id", null) as string | null;
     const store = useStore();
     const updateIndex = (index: number) => {
       if(id === null)
         return;
       store.commit(MUTATIONS.SET_GALLERY_INDEX, {id, index})
     }
     const syncIndex = computed(() => {
       if(id === null)
         return 0;
       store.getters[GETTERS.GET_GALLERY_INDEX](id)
     });
     return {id, updateIndex, syncIndex};
  },


  provide(){
    return {
      containerSize: computed(() => this.containerSize)
    }
  },


  mounted() {
    this.list.addEventListener('transitionend', () => {
        this.isAnimated = false;
    });
  },

  computed: {
    list(): HTMLElement{
      return this.$refs.list as HTMLElement;
    },

    length(): number{
      return this.list?.children?.length || 0;
    },
  },

  methods: {
    updateContainerSize(rect: DOMRect){
      this.containerSize = {
        w: rect.width,
        h: rect.height
      }
      this.updatePositionFromIndex(undefined, false);
    },

    next(){
      this.setIndex(this.index + 1)
      this.updatePositionFromIndex();
    },
    prev(){
      this.setIndex(this.index - 1)
      this.updatePositionFromIndex();
    },

    touchStart(event: TouchEvent){
      let list = this.$refs.list as HTMLElement;
      list = list as HTMLElement;

      const startX = event.touches[0]?.clientX;
      const startPosition = this.position;
      let shiftX = 0;

      const boundPosition = (position: number) => {
        const max = this.containerSize.w * 0.05;
        const min = (this.length- 1) * -this.containerSize.w - max;
        return toRange(position, min, max)
      }

      const touchMove = (event: TouchEvent) => {
        if(event.cancelable)
          event.preventDefault();
        event.stopPropagation();

        const clientX = event.touches[0]?.clientX - startX;
        const position = boundPosition(startPosition + clientX);
        this.updatePosition(position, false);
        shiftX = clientX;
      }

      const finishDragging = () => {
        if(!shiftX) return;
        shiftX < 0
          ? this.next()
          : this.prev();
      }

      list.addEventListener('touchmove', touchMove, {passive: false} as EventListenerOptions);
      list.addEventListener('touchend', function touchEnd(){
        list.removeEventListener('touchmove', touchMove, {passive: false} as EventListenerOptions);
        list.removeEventListener('touchend', touchEnd);
        finishDragging()
      })
    },

    setIndex(index: number){
       const nextIndex = toRange(index, 0 , this.length - 1);
       if(nextIndex === 0){
         this.prevDisabled = true;
       } else if(nextIndex === this.length - 1){
         this.nextDisabled = true;
       } else {
         this.prevDisabled = false;
         this.nextDisabled = false;
       }
      this.updateIndex(nextIndex)
      this.index = nextIndex;
      return nextIndex;
    },

    getPosition(index: number){
        return this.containerSize.w * -index;
    },

    updatePositionFromIndex(index?: number, animate = true){
      index = index || this.index;
      const position = this.getPosition(index);
      this.updatePosition(position, animate);
    },

    updatePosition(position: number, animate = true){
      this.isAnimated = animate;
      this.list.style.transform = `translateX(${position}px)`
      this.list.style.transitionProperty = animate ? "transform" : "none";
      this.position = position;
    }
  },

  watch:{
    syncIndex(){
      if(this.isAnimated) return;
      this.updatePositionFromIndex(this.syncIndex, false);
    }
  }
})
</script>
<style lang="scss">
.gallery{
  &__container{
    overflow: hidden;
  }
  &__list{
    display: flex;
    list-style: none;
    will-change: transfrom;
    transition-duration: .4s;
    transition-timing-function: ease-in-out;
  }

}
</style>
