import {provide, reactive, ref} from "vue";
import shallowArrayEqual from "@/utils/shallow-array-compare";


export type ErrorList = Array<{
    message: string;
    field: string;
}>

export type HTMLFormField = HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement | HTMLButtonElement ;

type FormControlsCollection = HTMLFormControlsCollection & {
    [key: string]: HTMLFormField;
}


declare global{
    interface Window{
        validationMessages: {
            [key in keyof ValidityState]: string;
        };
    }
}

export default function useFormValidation(
    validationMessageFail: string,
    validationMessageSuccess: string,
    errorMessage: string,
){
    let form = {} as  HTMLFormElement;
    const fieldsMap = new Map<string, HTMLFormField>();
    const validationErrors = reactive<{ list: ErrorList }>({list: [] as ErrorList});
    const message =  ref("");
    const isSuccessMessage = ref(false);


    const clearValidation = () => {
        message.value = ""
        fieldsMap.forEach((element) => {
            const label = element?.closest('label')
            label?.removeAttribute('data-validation-msg');
        })
        validationErrors.list = [] as ErrorList;
    };

    const setValidationMessages = (errors: ErrorList) => {
        validationErrors.list = errors;
        isSuccessMessage.value = false;

        if(errors.find(error => error.field === "_server")){
            message.value = errorMessage
        } else if(errors.length) {
            message.value= validationMessageFail
        } else {
            message.value= ""
        }

        errors.forEach(({message, field}) => {
            const formElement = fieldsMap.get(field);
            const label = formElement?.closest('label')
            label?.setAttribute('data-validation-msg', message);
        })
    };

    const setSuccessMessage = () => {
        message.value= validationMessageSuccess;//"The message has reached me, I will contact back to you.";
        isSuccessMessage.value = true;
        fieldsMap.forEach(element => {
            (element as HTMLFormField).value = ""
        })
    };


    const clientValidation = (element: HTMLFormField) => {
        if(!(element instanceof HTMLElement))
            return;
        element.addEventListener('invalid', (event: Event) => {
            event.preventDefault();

            const id = (event.target as HTMLFormField).getAttribute("id");
            const name =
                (event.target as HTMLFormField).getAttribute("aria-label") ||
                (event.target as HTMLFormField).getAttribute("data-label") ;

            if(!id || !name)
                return;

            let message = '';
            Object.entries(window.validationMessages).forEach(([state, msg]: [string, string]) => {
                if((event.target as HTMLFormField).validity[state as keyof ValidityState]){
                    message = msg.replace('[field]', name.toLowerCase())
                }
            })

            setValidationMessages([...validationErrors.list.filter(error => error.field !== id), {field: id, message}]);
        });

        element.addEventListener('input', (event: Event) => {
            const element = event.target as HTMLFormField;
            if(!element.checkValidity())
                return
            const id = element.getAttribute("id");
            const _validationErrors = validationErrors.list.filter(error => error.field !== id)
            if(!shallowArrayEqual(_validationErrors, validationErrors.list))
                setValidationMessages(_validationErrors)
        });
    };

    provide('registerFieldId', (id: string)  =>{
        fieldsMap.set(id, {} as HTMLFormField)
    })

    provide('validationErrors', validationErrors)

    const setFormRef = (_form: HTMLFormElement) => {
        form = _form;
        const elements = form.elements as FormControlsCollection;
        fieldsMap.forEach((field: HTMLFormField, id: string) => {
            fieldsMap.set(id, elements[id])
            clientValidation(elements[id])
        })
    }

    return {
        message: message,
        isSuccessMessage: isSuccessMessage,
        validationErrors: validationErrors,
        fieldsMap: fieldsMap,
        clientValidation,
        setSuccessMessage,
        setValidationMessages,
        clearValidation,
        setFormRef,
    }
}