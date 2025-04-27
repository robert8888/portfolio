import { load } from 'recaptcha-v3';

declare global {
    interface Window {
        gCaptchaPublicKey: string;
    }
}

export default async function getCaptchaToken(): Promise<string> {
    const recaptcha = await load(window.gCaptchaPublicKey, { autoHideBadge: true });

    return new Promise<string>((resolve, reject) => {
        grecaptcha.ready(() => {
            recaptcha.execute('login')
                .then((token) => resolve(token as string))
                .catch(reject);
        });
    });
}
