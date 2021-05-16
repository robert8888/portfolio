import {App, Component,  createApp} from "vue";

interface VuePlugin {
    install(app: App): void;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Components = Record<string, Component<any, any, any, Record<string, any>>>;

export default function defineVueComponent(components: Components, plugins: VuePlugin[]): void{
    customElements.define('vue-component', class extends HTMLElement{
        private app: App | undefined;

        createComponent(){
            this.app = createApp({ components })
            this.applyPlugins(this.app, plugins)
            this.setAttribute("data-server-rendered", "true");
            this.app.mount(this, true);
        }

        applyPlugins(app: App, plugins: VuePlugin[]){
            plugins.forEach((plugin: VuePlugin) => {
                app.use(plugin);
            })
        }

        connectedCallback(){
            this.createComponent();
        }

        disconnectedCallback(){
            if(!this.app) return;
            this.app.unmount()
        }
    })
}