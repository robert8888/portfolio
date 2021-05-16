import { load } from 'recaptcha-v3';

declare global {
    interface Window {
        gCaptchaPublicKey: string;
    }
}
export default async function getCaptchaToken(): Promise<string>{
    const recaptcha = await load(
        window.gCaptchaPublicKey,
        { autoHideBadge: true })

    return  await recaptcha.execute('login') as string;
}