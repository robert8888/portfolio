import {customAlphabet} from "nanoid";

export default function nanoid(): string{
    const nanoid = customAlphabet('ABCDEFGHIJKLMNOPRSQTUVWXZ0123456789', 8);
    return nanoid();
}