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
      const defaultSlot = this.$slots.default();
      return defaultSlot[0].children.map((node, index) => {
        node.props = {... node.props, index};
        return node;
      })
    },
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