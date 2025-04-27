export class BraveShieldsCaptchaError extends Error {
    constructor(message?: string) {
        super(message);
        Object.setPrototypeOf(this, BraveShieldsCaptchaError.prototype);
    }
}

export class BrowserSettingsCaptchaError extends Error {
    constructor(message?: string) {
        super(message);
        Object.setPrototypeOf(this, BrowserSettingsCaptchaError.prototype);
    }
}

export class CaptchaError extends Error {
    constructor(message?: string) {
        super(message);
        Object.setPrototypeOf(this, CaptchaError.prototype);
    }
}



export async function handleCaptchaError(): Promise<void> {
    const isBrave = await detectBraveBrowser();
    const isCaptchaLoaded = typeof grecaptcha !== 'undefined' && typeof grecaptcha.execute === 'function';

    if (!isCaptchaLoaded) {
        const googleAccessible = await testGoogleRecaptchaAccess();
        if (isBrave && !googleAccessible) {
            throw new BraveShieldsCaptchaError();
        } else {
            throw new BrowserSettingsCaptchaError();
        }
    }
    throw new CaptchaError();
}


async function detectBraveBrowser(): Promise<boolean> {
    if ((navigator as any).brave && typeof (navigator as any).brave.isBrave === 'function') {
        try {
            return await (navigator as any).brave.isBrave();
        } catch {
            return false;
        }
    }
    return false;
}

async function testGoogleRecaptchaAccess(): Promise<boolean> {
    return new Promise<boolean>((resolve) => {
        const img = new Image();
        img.src = 'https://www.gstatic.com/recaptcha/api2/logo_48.png';
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);

        // Timeout safety
        setTimeout(() => resolve(false), 3000);
    });
}
