import { load } from 'recaptcha-v3';

export default async function getCaptchaToken(): Promise<string>{
    const recaptcha = await load(
        (window as any).gCaptchaPublicKey,
        { autoHideBadge: true })

    return  await recaptcha.execute('login') as string;
}