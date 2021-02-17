<template  v-slot:item>
    <li class="navigation__item">
        <slot/>
    </li>
</template>

<script lang="ts">
import { defineComponent} from 'vue';


export default defineComponent({
  // props:{
  //   href: String,
  // },
  //
  // data: function(){
  //   return {
  //     href: this.href
  //   }
  // },

  // setup(){
  //
  // }

})


</script>
