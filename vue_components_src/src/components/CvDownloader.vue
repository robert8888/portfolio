<template>
  <div>
    <button @click="start">{{downloadLabel}}</button>
  </div>
  <modal :open="modalOpen" @close="modalOpen = false" :class="['cv-configurator', 'step--' + step]" :backdrop-close="false">
    <div class="cv-configurator__container">
      <div v-if="step === PROCESS_STEP.Configuration">
        <slot name="configurator"/>
      </div>
      <div v-if="step === PROCESS_STEP.Identification" class="cv-configurator__form-container">
        <div>
          <custom-from ref="form" @submit="submit" @mounted="recruiterFormMounted">
            <slot name="form"/>
            <div class="cv-configurator__btn-container">
              <button type="submit">{{downloadLabel}}</button>
            </div>
          </custom-from>
        </div>
      </div>
      <div v-if="step === PROCESS_STEP.Download">
        <cv-preloader :download-label="downloadLabelShort"
                      :spinner-label="spinnerLabel"
                      :open-label="openLabel"
                      @finish="modalOpen = false"
                      :brave-shields-captcha-error-message="braveShieldsCaptchaErrorMessage"
                      :browser-settings-captcha-error-message="browserSettingsCaptchaErrorMessage"
                      :captcha-error-message="captchaErrorMessage"
                      :unknown-error-message="unknownErrorMessage"/>
      </div>
    </div>
  </modal>
</template>
<script lang="ts">
import {computed, defineComponent, ref} from "vue"
import Modal from "@/components/Modal.vue";
import {default as CustomFrom} from "@/components/Form.vue";
import useFormValidation from "@/hooks/useFormValidation";
import {ACTIONS, GETTERS, useStore} from "@/store";
import {PROCESS_STEP, Recruiter} from "@/store/modules/cv";
import useFromDataMapper from "@/hooks/useFromDataMapper";
import CvPreloader from "@/components/CvPreloader.vue"
import HandleCaptchaErrorMixin from '@/mixins/handleCaptchaError'


export default defineComponent({
  components: {Modal, CustomFrom, CvPreloader},

  mixins: [HandleCaptchaErrorMixin],

  props:{
    downloadLabel:{
      type: String,
      default: 'Download'
    },
    downloadLabelShort:{
      type: String,
      default: 'Download'
    },
    spinnerLabel: {
      type: String,
      default: 'Preparing',
    },
    openLabel:{
      type: String,
      default: 'Open'
    },
  },


  setup(){
    const store = useStore();
    const step = computed(() => store.getters[GETTERS.GET_CV_PROCESS_STEP] as PROCESS_STEP)
    const restart = () => store.dispatch(ACTIONS.RESTART_CV_DOWNLOAD_PROCESS)
    const setRecruiterData = (data: Recruiter) => store.dispatch(ACTIONS.CONFIRM_RECRUITER, data)
    return {
      ...useFormValidation('', '',''),
      ...useFromDataMapper(),
      form: ref(null),
      step,
      restart,
      setRecruiterData
    }
  },

  data(){
    return {
      PROCESS_STEP:PROCESS_STEP,
      modalOpen: false,
    }
  },

  methods:{
    start(){
      this.restart();
      this.modalOpen = true;
      console.log(this)
    },
    recruiterFormMounted(form: HTMLFormElement){
      this.setFormRef(form)
    },
    async submit(e: Event){
      e.preventDefault()
      this.clearValidation();
      const data = this.getData(this.fieldsMap);
      this.setRecruiterData({
        email: data.emailField,
        company: data.companyField,
      } as Recruiter)
    },
  },
})

</script>