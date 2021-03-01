export type AnimationKeyframes = {
    [key: string]: {
        element: {
            children?: number;
            selector?: string;
        }
        attribute: "string";
        values: string[];
        duration: string;
        fill: string;
        keyTimes?: string;
    }[];
}