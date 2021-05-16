import {HTMLFormField} from "@/hooks/useFormValidation";

export default function useFromDataMapper(): {getData: (fieldsMap: Map<string, HTMLFormField>) => Record<string, string>}{
    return {
        getData(fieldsMap: Map<string, HTMLFormField>): Record<string, string>{
            const data = [...fieldsMap].reduce((data, [id, element]) => ({
                ...data,
                [id]: (element as HTMLFormField).value
            }), {})
            return data;
        }
    }
}