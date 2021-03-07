// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default function shallowArrayEqual(listA: any[], listB: any[]): boolean{
    return listA.every(item => listB.includes(item))
        && listB.every(item => listA.includes(item))
}