<script>
import { h, defineComponent} from 'vue'

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
    }
  },

  setup(props, { slots, attrs, emit }) {
    let clones = [];
    const defaultSlot = slots.default();
    for (let i = 0; i < props.times - 1; i++) {
      clones = [...clones, (defaultSlot.map(node => Object.assign({}, node)))]
    }

    if(typeof props.initialItems === "function")
        props.initialItems(defaultSlot[0]?.children?.length)

    return () =>
        h(
            props.is,
            {class: props.class},
            [...defaultSlot, ...clones]
        )
  }
})

</script>