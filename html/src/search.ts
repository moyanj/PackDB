import { DB } from "./data";

export class Engine extends DB {
    q: string
    constructor(q: string) {
        super()
        this.q = q;
    }
    async load() {
        try {
            let res = await fetch(this.baseURL + "/search?q=" + this.q)
            this.pack_list = await res.json() as Array<string>
        } catch (error) {
            console.error(error)
            this.pack_list = []
        }
        this.pageNum = Math.ceil(this.pack_list.length / 10);
    }
}