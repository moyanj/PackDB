interface PackageInfo {
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
    doc_type: string;
    latest: string;
    keywords: string[];
    releases: string[];
}

interface DBType { [key: string]: PackageInfo }

class DB {
    db: DBType;
    array: Array<{ name: string, data: PackageInfo }>;
    pageSize: number; // 每页显示的条目数
    pageNum: number; // 总页数
    currentPage: number; // 当前页码

    constructor() {
        this.db = {};
        this.array = [];
        this.pageSize = 10; // 默认每页10条数据
        this.pageNum = 0;
        this.currentPage = 1; // 默认显示第一页
    }

    async load() {
        this.db = await import("./assets/db.json") as unknown as DBType;
        this.array = Object.entries(this.db).map(([name, info]) => ({ name, data: info }));
        this.pageNum = Math.ceil(this.array.length / this.pageSize);
    }

    /*
        async load(): Promise<void> {
            try {
                // 获取当前版本号
                const currentVersion = await this.getVersion();
                // 检查本地缓存
                const cachedVersion = localStorage.getItem("pdb_dbver");
                if (cachedVersion === currentVersion) {
                    console.log('Using cached data');
                    const cachedData = localStorage.getItem("pdb_db");
                    this.db = cachedData ? JSON.parse(cachedData) : {};
                    this.array = Object.entries(this.db).map(([name, info]) => ({ name, data: info }));
                    this.pageNum = Math.ceil(this.array.length / this.pageSize);
                } else {
                    // 下载新的数据库文件
                    await this.downloadDatabase();
                    // 更新本地存储
                    localStorage.setItem("pdb_dbver", currentVersion);
                    localStorage.setItem("pdb_db", JSON.stringify(this.db));
                }
            } catch (error) {
                console.error('Request or parsing failed with error: ', error);
                this.db = {};
                this.array = [];
                throw error;
            }
        }
    
        async getVersion(): Promise<string> {
            return new Promise((resolve, reject) => {
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/ver.txt', true);
                xhr.onload = () => {
                    if (xhr.status === 200) {
                        resolve(xhr.responseText.trim());
                    } else {
                        reject(new Error('Failed to get version'));
                    }
                };
                xhr.onerror = () => {
                    reject(new Error('Network error'));
                };
                xhr.send();
            });
        }
    
        async downloadDatabase(): Promise<void> {
            return new Promise((resolve, reject) => {
                const xhr = new XMLHttpRequest();
                xhr.open('GET', '/db.msgpack', true);
                xhr.responseType = 'arraybuffer';
                xhr.onload = () => {
                    if (xhr.status === 200) {
                        const data = decode(new Uint8Array(xhr.response));
                        this.db = data;
                        this.array = Object.entries(data).map(([name, info]) => ({ name, data: info })) as  Array<{ name: string, data: PackageInfo }>;
                        this.pageNum = Math.ceil(this.array.length / this.pageSize);
                        resolve();
                    } else {
                        reject(new Error('Failed to download database'));
                    }
                };
                xhr.onerror = () => {
                    reject(new Error('Network error'));
                };
                xhr.send();
            });
        }
    */
    toArray() {
        return this.array;
    }

    // 获取当前页的数据
    getCurrentPageData(): Array<{ name: string, data: PackageInfo }> {
        const start = (this.currentPage - 1) * this.pageSize;
        const end = this.currentPage * this.pageSize;
        return this.array.slice(start, end);
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
        return this.array.length;
    }

    get(name: string): PackageInfo | null {
        if (name in this.db) {
            return this.db[name]
        }
        return null;
    }
}

export const db = new DB();