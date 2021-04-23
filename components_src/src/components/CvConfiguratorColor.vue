<template>
  <div :class="['color-profile', {'color-profile--current': profileId === currentId}]"
       @click="setAsCurrent">
    <div class="color-profile__wrapper">
      <ul class="color-profile__color-pair">
        <li v-for="colorPair in colorsToDisplay" :key="colorPair.join('-')">
          <div v-for="colorName in colorPair"
               :style="{'--color': colors[colorName]}"
               :class="'color-profile__color color-profile__color--' + colorName.split(/(?=[A-Z])/).map(s=>s.toLowerCase()).join('-')"
               :key="colorName"/>
        </li>
      </ul>
      <h6 class="color-profile__name">{{name}}</h6>
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent, computed} from "vue";
import {ACTIONS, GETTERS, MUTATIONS, useStore} from "@/store";


export default defineComponent({
  props: {
    name:{
      type: String,
      required: true,
    },
    colors: {
      type: Object,
      required: true
    },
    profileId:{
      type: String,
      required: true,
    },
    default: {
      type: Boolean,
    }
  },


  setup(props){
    const store = useStore();
    const currentId = computed(() => store.getters[GETTERS.GET_CV_COLOR_PROFILE_ID]);
    const setAsCurrent = () => {
      store.commit(MUTATIONS.SET_CV_COLOR_PROFILE, {
        id: props.profileId,
        colors: props.colors
      })
    }
    if(props.default){
      store.commit(ACTIONS.SET_CV_INIT_COLOR_PROFILE, {
        id: props.profileId,
        colors: props.colors
      })
    }
    return {
      currentId,
      setAsCurrent,
    }
  },

  data(){
    return {
      colorsToDisplay:[
        ['background', 'text'],
        ['primary','textPrimary'],
        ['secondary','textSecondary']
      ]
    }
  },

})
</script>