export default function arrayTake<T>(arr: T[], indexes: number[]): T[]{
    return indexes.reduce((result, index) => {
        result.push(arr[index]);
        return result;
    }, new Array<T>())
}

