import {defineComponent, PropType} from "vue"


export default defineComponent({
    props: {
        braveShieldsCaptchaErrorMessage: {
            type: String,
            default: 'Your Brave browser is blocking CAPTCHA. Please disable Shields for this site.',
        },
        browserSettingsCaptchaErrorMessage: {
            type: String,
            default: 'Your browser settings are blocking CAPTCHA. Check ad blockers or privacy settings.',
        },
        captchaErrorMessage: {
            type: String,
            default: 'An error occurred while loading CAPTCHA. Please try again.',
        },
        unknownErrorMessage: {
            type: String,
            default: 'An unexpected error occurred. Please try again later.',
        },
    },

    methods:{
        getErrorMessage(error: Error){
            switch(error.constructor.name){
                case 'BraveShieldsCaptchaError':
                    return this.braveShieldsCaptchaErrorMessage;
                case 'BrowserSettingsCaptchaError':
                    return this.browserSettingsCaptchaErrorMessage;
                case 'CaptchaError':
                    return this.captchaErrorMessage;
                default:
                    return this.unknownErrorMessage;
            }
        }
    }
})