<template>
  <div ref="container">
  <slot/>
  </div>
  <modal :open="modalOpen" @close="modalOpen = false" class="pdf-downloader">
    <div class="pdf-downloader__spinner-wrapper">
      <spinner v-if="isLoading" :label="spinnerLabel"/>
    </div>
    <div class="pdf-downloader__button-wrapper" v-if="!isLoading">
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
  </modal>
</template>
<script lang="ts">
import {defineComponent} from "vue";
import Modal from "./Modal.vue";
import Spinner from "@/components/Spinner.vue";
import {getRequest} from "@/api/backend_api";
import {getResponseFilename} from "@/utils/get_response_filename";

type EventCallback = (this: HTMLElement, ev: MouseEvent) => void;
type EventMap = Map<HTMLElement, {[key: string]: EventCallback}>;
type EventName = 'click';


interface ComponentData{
  eventMapping: Map<HTMLElement, {[key: string]: EventCallback}>;
  modalOpen: boolean;
  isLoading: boolean;
  pdfBlobData: Blob | null;
  pdfFilename: string;
}

export default defineComponent({
  components: {Modal, Spinner},

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
    }
  },

  data(): ComponentData{
    return {
      eventMapping: new Map<HTMLElement, {[key: string]: EventCallback}>(),
      modalOpen: false,
      isLoading: true,
      pdfBlobData: null,
      pdfFilename: ''
    }
  },

  mounted() {
    const items = this.grabItems(this.$refs.container as HTMLElement)
    this.eventMapping = items.reduce((map, el: HTMLElement) => {
       map.set(el, {
         'click': this.onAnchorClick.bind(this),
       })
      return map;
    }, new Map<HTMLElement, {[key: string]: EventCallback}>())

    this.attachEvents(this.eventMapping)
  },

  beforeUnmount(){
   this.deAttachEvent(this.eventMapping)
  },

  methods:{
    grabItems(container: HTMLElement): HTMLElement[]{
      return Array.from(container.querySelectorAll('[data-download-pdf]') || [] as HTMLElement[])
    },
   *iterateEventMap(eventMap: EventMap): IterableIterator<[HTMLElement, EventName, EventCallback]>{
     for(let [input, events] of eventMap.entries()){
       for(let eventName in events){
         yield [input, eventName as EventName, events[eventName] as EventCallback]
       }
     }
    },
    attachEvents(eventMap: EventMap): void{
      for (let [input, eventName, callback] of this.iterateEventMap(eventMap)){
        input.addEventListener(eventName, callback)
      }
    },
    deAttachEvent(eventMap: EventMap): void{
      for (let [input, eventName, callback] of this.iterateEventMap(eventMap)){
        input.removeEventListener(eventName, callback)
      }
    },
    onAnchorClick(ev: MouseEvent): void{
      ev.preventDefault();
      this.modalOpen = true;

      const url = (ev.target as HTMLElement).getAttribute('href');
      if(!url)
        return;
      this.fetchPdf(url)
    //
    },

    async fetchPdf(path: string): Promise<any>{
      this.isLoading = true;
      const response = await getRequest(path)
      this.pdfBlobData = await response.blob();
      this.pdfFilename = getResponseFilename(response)
      this.isLoading = false;
    },

    getDownloadElement(blob: Blob): HTMLAnchorElement{
      const a = document.createElementNS("http://www.w3.org/1999/xhtml", "a") as HTMLAnchorElement;
      const url = URL.createObjectURL(blob)
      a.href = url;
      return a;
    },

    onButtonClick(actionName: string){
      if(!this.pdfBlobData)
        return;

      if(actionName === 'download')
        this.downloadBlob();

      this.openBlob();
      this.modalOpen = false;
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


})
</script>