<template>
  <div class="gallery">
     <div class="gallery__container" ref="container" v-size="updateContainerSize">
        <ul class="gallery__list" ref="list" v-on:touchstart.passive="touchStart">
          <slot/>
        </ul>
       <div class="gallery__controls">
         <button class="gallery__controls__btn" @mouseup="prev" tabindex="-1"/>
         <button class="gallery__controls__btn" @mouseup="next" tabindex="-1"/>
       </div>
     </div>
  </div>
</template>

<script lang="ts">
import {computed, defineComponent} from 'vue';
import toRange from "@/utils/toRange";


export default defineComponent({
  data(){
    return {
      containerSize: {
        w: 0,
        h: 0,
      },
      index: 0,
      position: 0,
      isDragged: false,
      length: 0,
    }
  },
  provide(){
    return {
      containerSize: computed(() => this.containerSize)
    }
  },

  mounted() {
    this.length = (this.$refs.list as HTMLElement).children.length
  },

  methods: {
    updateContainerSize(rect: DOMRect){
      this.containerSize = {
        w: rect.width,
        h: rect.height
      }
      this.updatePosition();
    },

    next(){
      this.index = toRange(this.index + 1, 0 , this.length - 1);
      this.updatePosition();
    },
    prev(){
      this.index = toRange(this.index - 1, 0 , this.length - 1);
      this.updatePosition();
    },

    touchStart(event: TouchEvent){
      this.isDragged = true;
      //@ts-ignore
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
        const clientX = event.touches[0]?.clientX - startX;
        this.position = boundPosition(startPosition + clientX);
        shiftX = clientX;
      }

      const finishDragging = () => {
        this.isDragged = false;
        if(!shiftX) return;
        shiftX < 0
          ? this.next()
          : this.prev();
      }

      list.addEventListener('touchmove', touchMove, {passive: false});
      list.addEventListener('touchend', function touchEnd(){
        //@ts-ignore
        list.removeEventListener('touchmove', touchMove, {passive: false});
        list.removeEventListener('touchend', touchEnd);
        finishDragging()
      })
    },

    updatePosition(){
      this.position = this.containerSize.w * -this.index
    }
  },

  watch: {
    position(){
      (this.$refs.list as HTMLElement).style.transform = `translateX(${this.position}px)`
    },
    isDragged(){
     this.isDragged
        ? (this.$refs.list as HTMLElement).style.transition = 'none'
        : (this.$refs.list as HTMLElement).style.transition = 'transform 1s ease'
    }
  }

})
</script>
<style lang="scss">
.gallery{
  &__container{
    overflow-x: hidden;
  }
  &__list{
    display: flex;
    transition: transform 1s ease;
    list-style: none;
  }

}
</style>
