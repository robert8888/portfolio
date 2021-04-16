import {customAlphabet} from "nanoid";

export default function nanoid(): string{
    const nanoid = customAlphabet('ABCDEFGHIJKLMNOPRSQTUVWXZ', 8);
    return nanoid();
}