import { load } from 'recaptcha-v3';

declare global {
    interface Window {
        gCaptchaPublicKey: string;
    }
}
export default async function getCaptchaToken(): Promise<string>{
    console.log("the public key", window.gCaptchaPublicKey)

    const recaptcha = await load(
        window.gCaptchaPublicKey,
        { autoHideBadge: true })


    await recaptcha.execute('login') as string;
    return "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
}