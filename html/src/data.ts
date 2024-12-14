export interface ReleasesFileInfo {
    size: number;
    upload_time: number;
    file_name: string;
    digests: {
        md5: string,
        sha256: string,
        blake2b_256: string
    }
    
}

export interface ReleasesInfo {
    name: string;
    files: Array<ReleasesFileInfo>;

}

export interface PackageInfo {
    desc: string;
    url: string;
    requires: string[];
    author: string;
    author_email: string;
    home_page: string;
    requires_python: string;
    classifiers: string[];
    pypi_desc: string;
    project_urls: { [key: string]: string };
    add_time: number;
    doc: string;
    doc_html: string;
    latest: string;
    keywords: string[];
    releases: ReleasesInfo[];
}

class DB {
    pack_list: Array<string>;
    baseURL: string; // 每页显示的条目数
    pageNum: number; // 总页数
    currentPage: number; // 当前页码

    constructor() {
        this.pack_list = [];
        this.pageNum = 0;
        this.currentPage = 1; // 默认显示第一页
        this.baseURL = "http://127.0.0.1:8000"
    }

    async load() {
        this.pack_list = await (await fetch(this.baseURL + "/packs")).json() as Array<string>
        this.pageNum = Math.ceil(this.pack_list.length / 10);
    }

    // 获取当前页的数据
    async getCurrentPageData(): Promise<Array<{ name: string, data: PackageInfo }>> {
        const start = (this.currentPage - 1) * 10;
        const end = this.currentPage * 10;
        const names = this.pack_list.slice(start, end).join(",")
        console.log(names)
        var ret = await (await fetch(this.baseURL + "/batch?l=" + names)).json()
        ret = Object.entries(ret).map(([name, info]) => ({ name, data: info }));

        return ret
    }



    // 切换到下一页
    nextPage(): boolean {
        if (this.currentPage < this.pageNum) {
            this.currentPage++;
            return true;
        }
        return false;
    }

    // 切换到上一页
    prevPage(): boolean {
        if (this.currentPage > 1) {
            this.currentPage--;
            return true;
        }
        return false;
    }

    // 跳转到指定页码
    goToPage(page: number): boolean {
        if (page > 0 && page <= this.pageNum) {
            this.currentPage = page;
            return true;
        }
        return false;
    }

    getLength(): number {
        return this.pack_list.length;
    }

    async get(name: string): Promise<PackageInfo> {
        let f = await fetch(this.baseURL + "/pack/" + name)
        return await (await f.json()).info as unknown as PackageInfo
    }
}

export const db = new DB();