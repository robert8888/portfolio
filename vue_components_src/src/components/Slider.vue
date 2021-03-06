<template>
  <div class="slider" >
    <div class="slider__container"
         ref="container"
         v-size="updateContainerSize">
        <node-cloner
            is="ul"
            :times="times"
            :initial-items="setNumberOfInitialItems"
            @click="catchExpandIndex"
            class="slider__list"
            ref="list">
          <slot/>
        </node-cloner>
    </div>
    <div class="slider__controls">
      <button @click="next" class="slider__controls__btn slider__controls__btn--next" aria-label="next"/>
      <button @click="prev" class="slider__controls__btn slider__controls__btn--prev" aria-label="previous"/>
    </div>

  </div>
</template>
<script>
import {defineComponent, computed, nextTick} from "vue";
import {extractTransformX} from "@/utils/regexs";
import NodeCloner from "./NodeCloner";
import toRange from "@/utils/to-range";


export default defineComponent({
  components: {NodeCloner},

  props: {
     duration: {
       type: Number,
       default: 1000
     },
     minMargin: {
       type: Number,
       default: 20
     },
     wide:{
       type: Boolean,
       default: false
     },
     touchDiffChangeRatio:{
       type: Number,
       default: 1/5
     }
  },

  data(){
    return {
      containerSize: {},
      numberOfItems: 0,
      numberOfInitialItems: 0,
      numberOfVisibleItems: 0,
      visibleItemsIndexes: [],
      itemWidth: 0,
      itemMargin: 0,
      position: 0,
      correction: 0,
      index: 0,
      times: 3,
      
      lastExpandedCardIndex: null,
    }
  },


  provide(){
    return{
      itemMargin: computed(() => this.itemMargin),
      itemSizeChange: () => {/*no empty*/},
      visibleItems: computed(() => this.visibleItemsIndexes)
    }
  },

  mounted() {
    this.numberOfItems = this.list.children.length;
    window.addEventListener("touchstart", this.initTouchStart);
    this.list.addEventListener("transitionend",(e) => {
      if(e.target !== this.list)
        return;
      this.balance.call(this)
    });
  },

  unmounted() {
    window.removeEventListener("touchstart", this.initTouchStart)
  },

  computed: {
    itemSize(){return this.itemWidth + this.itemMargin * 2},

    list(){
      return this.$refs.list.$el;
    },

    numberOfHiddenItems(){
      return this.numberOfItems - this.numberOfVisibleItems;
    },

    startIndex(){
      return this.times === 1
        ? 0
        : -this.numberOfInitialItems;
    }
  },

  methods:{
    catchExpandIndex(e){
      if(e.target.matches(".card-project__btn--expand")){
        this.lastExpandedCardIndex =
            [...this.list.children].findIndex(child =>
                child === e.target.closest(".slider__item")
            )
      }
    },

    initTouchStart(e){
      if(e.target.closest(".slider__container"))
        this.touchStart(e);
    },

    setItemSwapHandler(handler){
      this.swapHanlder = handler;
    },

    setNumberOfInitialItems(itemNum){
      this.numberOfInitialItems = itemNum;
      this.index = -itemNum;
    },

    updateItemWidth(){
      const itemWidth = [...this.list.children].reduce((a,e,i)=>(a*i + e.clientWidth)/(i+1), 0);
      this.itemWidth = itemWidth;
      return itemWidth;
    },

    updateContainerSize(rect){
      this.containerSize = rect;
      this.updateItemWidth();
      this.index = -this.lastExpandedCardIndex || this.index;
      nextTick(() =>
          this.setPosition(this.getPositionFromIndex(this.index), false)
      );
    },

    updateVisibleIndexes(){
        const visible = new Array(this.numberOfVisibleItems).fill(0).map((_,i) => -this.index - this.numberOfInitialItems + i)
        this.visibleItemsIndexes = visible;
    },

    next(){
      this.setIndex(this.index + 1)
      this.setPositionToIndex(this.index);
    },

    prev(){
      this.setIndex(this.index - 1);
      this.setPositionToIndex(this.index);
    },

    getIndexFromPosition(position){
      const index = Math.round((position - this.correction) / this.itemSize);
      return toRange(index, -this.numberOfHiddenItems, 0)
    },

    setIndex(index) {
      const min = -this.numberOfHiddenItems;
      const max = 0;
      this.index = toRange(index, min, max);
    },

    getCurrentPosition(){
      return window.getComputedStyle(this.list).transform?.match(extractTransformX)?.groups?.translate || 0;
    },

    getPositionFromIndex(index = this.index){
      return index * this.itemSize + this.correction;
    },


    setPositionToIndex(index = this.index, animated = true){
      const targetPosition = this.getPositionFromIndex(index)
      this.setPosition(targetPosition, animated)
    },

    updateStyle(position, animated){
       this.list.style =  `transform: translateX(${position}px); transition: ${animated ? "transform .4s" : "none"}`;
    },

    setPosition(position, animated = true){
      const min = this.times === 1
          ? - this.itemSize / 3
          : -this.numberOfHiddenItems * this.itemSize - this.itemSize / 3;
      const max = this.itemSize / 3
      position = toRange(position, min, max);
      this.updateStyle(position, animated)
      this.position = position;
    },


    balancedIndex(index){
      let nextIndex = index;
      if(index === 0){
        nextIndex = this.times ===  1 ? 0 :  -this.numberOfInitialItems;
      } else if(index <= -this.numberOfInitialItems * (this.times - 1)){
        nextIndex = this.times ===  1 ? 0 : -this.numberOfInitialItems + (index % this.numberOfInitialItems);
      }
      return nextIndex;
    },

    balance(nextIndex){
      const _nextIndex = nextIndex || this.balancedIndex(this.index);
      this.setPosition(this.getPositionFromIndex(_nextIndex), false)
      this.index = _nextIndex;
    },

    touchStart(event){
      if(event.cancelable)
        event.preventDefault();

      const list = this.list;
      const lastAnimations = list.getAnimations() || [];
      const startPositionX = +this.getCurrentPosition();
      lastAnimations.forEach(a => a.cancel());

      this.setPosition(startPositionX, false);

      const startX = event.clientX || event.touches[0]?.clientX || 0;

      let wasDragged = false;
      let diffX = 0;
      const touchMove = (event) =>{
        const clientX = event.clientX || event.touches[0]?.clientX || 0;
        diffX = clientX - startX;
        this.setPosition(startPositionX + diffX, false);
        wasDragged = true;
      }

      const finishMove = () => {
        if(!wasDragged) return;
        const currentIndex = this.getIndexFromPosition(this.position);

        let move = 0;
        if(Math.abs(diffX) / this.itemWidth > this.touchDiffChangeRatio &&
           currentIndex === this.index
        ){
          move = diffX > 0 ? 1 : -1;
        }
        this.setIndex(currentIndex + move);
        this.setPositionToIndex(this.index);
      }

      window.addEventListener('touchmove', touchMove, {passive: false});
      window.addEventListener('touchend', function touchEnd(){
        window.removeEventListener('touchmove', touchMove, {passive: false});
        window.removeEventListener('touchend', touchEnd);
          finishMove();
      })
    }
  },

  watch: {
    containerSize(){
      const wideMode = false;
      const minMargin = this.minMargin;
      const width = this.containerSize.width;
      const itemWidth = this.itemWidth;
      // let visible = Math.floor((width - (2 * minMargin)) / (itemWidth + minMargin)) || 1
      let visible = Math.floor((width) / (itemWidth + minMargin)) || 1


      if(visible > this.numberOfInitialItems){
        visible = this.numberOfInitialItems;
        this.times = 1;
        this.setPosition(this.getPositionFromIndex(0))
        this.index = 0;
      } else if(this.times === 1) {
        this.times = 3
        this.index = this.startIndex;
      }

      if(this.wide && this.visible > 2){
        this.wideMode = true;
      }

      const marginSum = width - (visible * itemWidth);

      if(isNaN(marginSum))
        return;

      let margin = wideMode
          ? marginSum / (visible - 1 || 1) / 2
          : marginSum / visible / 2;

      if(margin < minMargin){
        margin = minMargin;
        this.correction = -minMargin + ((width - (itemWidth * visible)) / Math.max(visible, 2) / visible);
      } else {
        this.correction = wideMode ? -margin : 0;
      }

      this.numberOfVisibleItems = visible;
      this.itemMargin = margin;
      this.updateVisibleIndexes()
    },
    index(){
       this.updateVisibleIndexes()
    }
  }
})
</script>
<style lang="scss">
.slider{
  position: relative;
  &__container{
    overflow: hidden;
  }
  &__list{
    list-style: none;
    display: flex;
    will-change: transform;
  }
  &__controls{
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    transform: translateY(-50%);
    display: flex;
    justify-content: space-between;
    pointer-events: none;
  }
}
</style>