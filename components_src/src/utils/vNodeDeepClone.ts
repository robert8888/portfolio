// @ts-nocheck
export default function deepClone(vnodes, createElement){
    function cloneVNode(vnode) {
        let clonedChildren;
        if(vnode.children){
            if(vnode.children instanceof Array){
                clonedChildren = vnode.children.map(cloneVNode);
            }
            clonedChildren = vnode.children;
        }

        const cloned = createElement(vnode.tag, vnode.data, clonedChildren);
        cloned.text = vnode.text;
        cloned.isComment = vnode.isComment;
        cloned.componentOptions = vnode.componentOptions;
        cloned.el = vnode.el;
        cloned.context = vnode.context;
        cloned.ns = vnode.ns;
        cloned.isStatic = vnode.isStatic;
        cloned.key = vnode.key + Math.random().toFixed(2);
        cloned.type = vnode.type;
        return cloned;
    }

    return vnodes.map( cloneVNode );
}

// const DATA_KEYS = [
//     'class', 'staticClass', 'style',
//     'attrs', 'props', 'domProps',
//     'on', 'nativeOn',
//     'directives', 'scopesSlots',
//     'slot', 'ref', 'key'
// ]
//
// function mutateKey(key) {
//     return '' + key + `-cloned-cid`
// }
//
// function extractData(vnode, isComp) {
//     const data = _.pick(vnode.data, DATA_KEYS)
//     if (isComp) {
//         const cOpts = vnode.componentOptions
//         _.assign(data, {
//             props: cOpts.propsData,
//             on: cOpts.listeners
//         })
//     }
//
//     if (data.key) {
//         data.key = mutateKey(data.key)
//     }
//
//     return data
// }