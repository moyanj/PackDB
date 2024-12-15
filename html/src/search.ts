import { DB, PackageInfo } from "./data";

export class Engine extends DB {
    q: string
    constructor(q: string) {
        super()
        this.q = q;
    }
    async load() {
        this.pack_list = await (await fetch(this.baseURL + "/search?q=" + this.q)).json() as Array<string>
        this.pageNum = Math.ceil(this.pack_list.length / 10);
    }
}