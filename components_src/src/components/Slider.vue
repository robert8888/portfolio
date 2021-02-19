<template>
  <div class="slider">
    <div class="slider__container"
         ref="container"
         v-size="updateContainerSize"
         v-on:touchstart="touchStart">
      <div  >
        <node-cloner
            is="ul"
            :times="3"
            :initial-items="setNumberOfInitialItems"
            class="slider__list"
            ref="list"
            :style="translation" >
          <slot/>
        </node-cloner>
      </div>

    </div>
    <div class="slider__controls">
      <button @click="prev"
              class="slider__controls__btn slider__controls__btn--prev">
        pre
      </button>
      <button @click="next"
              class="slider__controls__btn slider__controls__btn--next">
        next
      </button>
    </div>

  </div>
</template>
<script>
import {defineComponent, computed} from "vue";
import {extractTransformX} from "@/utils/regexs";
import NodeCloner from "./NodeCloner";

export default defineComponent({


  props: {
     duration: {
       default: 1000
     }
  },

  data(){
    return {
      containerSize: {},
      numberOfItems: 0,
      itemWidth: 0,
      itemMargin: 0,
      position: 0,
      correction: 0,
      index: 0,
    }
  },

  components: {NodeCloner},

  provide(){
    return{
      containerSize: computed(() => this.containerSize),
      numberOfItems: computed(() => this.numberOfItems),
      onMargin: (margin, isMin) =>{
        this.itemMargin = margin;
        isMin
          ? this.correction = -margin
          : this.correction = 0
      }
    }
  },

  mounted() {
    this.numberOfItems = this.list.children.length;
  },

  computed: {
    itemSize(){return this.itemWidth + this.itemMargin * 2},
    translation(){
      return `transform: translateX(${this.position}px)`;
    },
    list(){
      return this.$refs.list.$el;
    }
  },

  methods:{
    setNumberOfInitialItems(number){
      this.numberOfInitalItems = number;
      this.index = -number;
    },
    updateContainerSize(rect){
      this.containerSize = rect;
      this.itemWidth = this.list.children[0].clientWidth;
      this.setPosition(this.getTargetPosition())
    },

    next(){
      this.index++;
      this.animatePosition(this.index);
    },

    prev(){
      this.index--;
      this.animatePosition(this.index);
    },

    getIndexFromPosition(position){
        return Math.round((position - this.correction) / this.itemSize);
    },

    getCurrentPosition(){
      return window.getComputedStyle(this.list).transform?.match(extractTransformX)?.groups?.translate || 0;
    },

    getTargetPosition(index = this.index){
      return index * this.itemSize + this.correction;
    },

    animatePosition(index = this.index){
      const list = this.list;
      const lastAnimation = list.getAnimations() || [];

      const currentPosition = +this.getCurrentPosition() || this.position;
      lastAnimation.forEach(a => a.cancel());

      const targetPosition = this.getTargetPosition(index)

      const distance = Math.abs(targetPosition - currentPosition)

      const duration = this.duration * distance / this.itemSize;

      const animation = list.animate([
        {transform: `translateX(${currentPosition}px)`},
        {transform: `translateX(${targetPosition}px)`},
      ], {
        duration: duration,
        fill: "forwards"
      });
      animation.onfinish = () => {
        this.position = targetPosition;
      }
    },

    setPosition(position){
      this.position = position;
    },

    balance(){
      console.log("duapte")
    },

    touchStart(event){
      if(event.cancelable)
        event.preventDefault();

      const list = this.list;
      const lastAnimations = list.getAnimations() || [];
      const startPosition = +this.getCurrentPosition();

      console.log("start position", startPosition, this.position)

      lastAnimations.forEach(a => a.cancel());
      this.setPosition(startPosition);

      const startX = event.clientX || event.touches[0]?.clientX || 0;

      const touchMove = (event) =>{
        const clientX = event.clientX || event.touches[0]?.clientX || 0;
        const diffX = clientX - startX;
        this.setPosition(startPosition + diffX)
      }

      const finishMove = () => {
          this.index = this.getIndexFromPosition(this.position);
          this.animatePosition(this.index);
      }

      list.addEventListener('touchmove', touchMove, {passive: false});
      list.addEventListener('touchend', function touchEnd(){
          list.removeEventListener('touchmove', touchMove, {passive: false});
          list.removeEventListener('touchend', touchEnd);
          finishMove();
      })
    }
  },


})
</script>
<style lang="scss">
.slider{
  &__container{
    overflow: hidden;
  }
  &__list{
    list-style: none;
    display: flex;
    will-change: transform;
  }
}
</style>