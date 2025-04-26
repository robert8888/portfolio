import { load } from 'recaptcha-v3';

declare global {
    interface Window {
        gCaptchaPublicKey: string;
    }
}

export default async function getCaptchaToken(): Promise<string> {
    console.log("the public key", window.gCaptchaPublicKey);

    const recaptcha = await load(window.gCaptchaPublicKey, { autoHideBadge: true });

    return new Promise<string>((resolve, reject) => {
        grecaptcha.ready(() => {
            recaptcha.execute('login')
                .then((token) => resolve(token as string))
                .catch(reject);
        });
    });
}
