<script>
import { h, defineComponent, reactive, ref} from 'vue'
import deepClone from "@/utils/vNodeDeepClone";

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
    swapItems:{
      type: Function,
    }
  },

  setup(props, { slots }) {
    const length = slots.default()?.[0].children?.length;

    if(typeof props.initialItems === "function")
        props.initialItems(length)

    return { length }
  },

  data(){
    return {
      shift: 0,
      scale: this.times,
    }
  },

  created(){
    if(typeof this.swapItems === "function"){
      this.swapItems(this.swap)
    }
  },


  methods:{
    swap(dir){ this.shift = dir; },

    swapFirstN: (arr, n) =>{
      console.log("first")
      for(let i = 0; i < Math.abs(n); i++){
        const first = arr.shift();
        arr.push(first);
      }
      return arr;
    },

    swapLastN: (arr, n) =>{
      for(let i = 0; i < Math.abs(n); i++){
        const last = arr.pop();
        arr.unshift(last);
      }
      return arr;
    },


    setKeys(nodes){
      return nodes.map((node, i) => {
        node.key = i;
        return node;
      })
    },
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
      let items = this.items.children;
      items = this.setKeys(items)
      if(this.times === 1) {
        return items.slice(0, this.length);
      }
      if(this.shift === 0) return items;


      // console.log("init ", this.shift, items)
      // let shifted = this.shift < 0
      //     ? this.swapLastN(items, this.shift)
      //     : this.swapFirstN(items, this.shift)
      // console.log("swapde", shifted);
      // console.log(items)


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