<script>
import { h, defineComponent } from 'vue'

export default defineComponent({
  name: "cloner",
  props: {
    times: {
      type: Number,
      default: 1
    },
    is: {
      type: String,
      required: true,
      default: "ul",
    },
    class: {
      type: String,
    },
    initialItems:{
      type: Function,
    },
  },

  setup(props, { slots }) {
    const length = slots.default()?.[0].children?.length;

    if(typeof props.initialItems === "function")
        props.initialItems(length)

    return { length }
  },

  data(){
    return {
      scale: this.times,
    }
  },



  computed:{
    items(){
      const defaultSlot = this.$slots.default();
      let clones = [...defaultSlot[0].children];
      for (let i = 0; i < this.scale - 1; i++) {
        const copy = defaultSlot[0].children.map(node => Object.assign({}, node))
        clones = clones.concat(copy);
      }
      defaultSlot[0].children = clones;
      return defaultSlot[0];
    },


    children() {
      const items = this.items.children;
      if(this.times === 1) {
        return items.slice(0, this.length);
      }
      return items;
    }
  },

  render(){
    return h(
        this.is,
        {class: this.class},
        this.children
    )
  }
})

</script>