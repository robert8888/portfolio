<template>
  <div class="cv-configurator__preloader">
    <div class="cv-configurator__spinner-wrapper" v-if="isLoading" >
      <spinner :label="spinnerLabel"/>
    </div>
    <div class="cv-configurator__button-wrapper" v-if="!isLoading && !fail">
      <button @click="onButtonClick('download')"
              class="btn btn--download"
              :disabled="isLoading">
        {{downloadLabel}}
      </button>
      <button @click="onButtonClick('open')"
              class="btn btn--open"
              :disabled="isLoading">
        {{openLabel}}
      </button>
    </div>
    <div class="cv-configurator__sad-smile-wrapper" v-if="fail">
      <i class="cv-configurator__sad-smile"/>
    </div>
  </div>
</template>
<script lang="ts">
import {computed, defineComponent} from "vue";
import Spinner from "@/components/Spinner.vue";
import {getCv, GetCVPayload} from "@/api/backend_api";
import {getResponseFilename} from "@/utils/get_response_filename";
import {GETTERS, store, useStore} from "@/store";

interface ComponentData{
  isLoading: boolean;
  fail: boolean;
  pdfBlobData: Blob | null;
  pdfFilename: string;
}


export default defineComponent({
  components: {Spinner},
  emits: ['finish'],
  props:{
    spinnerLabel: {
      type: String,
      default: 'Preparing',
    },
    downloadLabel:{
      type: String,
      default: 'Download'
    },
    openLabel:{
      type: String,
      default: 'Open'
    },
  },

  setup(){
    const store = useStore();
    const requestData = computed(() => store.getters[GETTERS.GET_CV_REQUEST_DATA] as GetCVPayload);
    return {requestData}
  },

  data(): ComponentData{
    return{
      isLoading: true,
      fail: false,
      pdfBlobData: null,
      pdfFilename: ''
    }
  },

  mounted() {
    this.fetchPdf();
  },

  methods:{
    async fetchPdf(): Promise<any>{
      this.fail = false;
      this.isLoading = true;
      try{
        const response = await getCv(this.requestData as GetCVPayload);

        const contentType = response.headers.get("content-type")
        if(contentType == "application/json"){
          const jsonData = await response.json();
          throw new Error(jsonData.errors)
        }

        this.pdfBlobData = await response.blob();
        this.pdfFilename = getResponseFilename(response)
        this.isLoading = false;
      } catch {
        this.fail = true;
      } finally {
        this.isLoading = false;
      }
    },

    onButtonClick(actionName: string){
      if(!this.pdfBlobData)
        return;

      if(actionName === 'download')
        this.downloadBlob();

      this.openBlob();
      this.$emit('finish')
    },

    downloadBlob(){
      const a = document.createElement("a");
      a.href = URL.createObjectURL(this.pdfBlobData);
      a.download = this.pdfFilename;
      a.click()
    },

    openBlob(){
      const url = URL.createObjectURL(this.pdfBlobData)
      window.open(url, '_blank')
    },
  },

  watch: {
    fail(){
      if(this.fail)
        setTimeout(() => this.$emit('finish'), 5000)
    }
  }
})
</script>