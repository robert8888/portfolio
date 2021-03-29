<script>
import { h, defineComponent } from 'vue'

export default defineComponent({
  name: "list",
  props: {
    is: {
      type: String,
      required: true,
      default: "ul",
    },
    class: {
      type: String,
    }
  },

  computed:{
    children(){
      const isFragment = type =>
          type.toString() === "Symbol(Fragment)" || type.toString() === "Symbol()" ;
      const defaultSlot = this.$slots.default?.();

      let node = defaultSlot[0];

      while(isFragment(node.type) && isFragment(node.children[0].type)){
        node = node.children[0];
      }

      return node.children.map((node, index) => {
        node.props = {...node.props, index: index };
        return node;
      })
    },
  },

  render(){
    return h(
        this.is,
        {
          class: this.class,
          ...this.$attrs
        },
        this.children
    )
  }
})

</script>