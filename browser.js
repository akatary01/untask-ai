const { chromium } = require('playwright');

class Browser {
    async init() {
        this.browser = await chromium.launch({ headless: false });
        this.page = await this.browser.newPage();
    }

    constructor() { this.init(); }

    async open(url) {
        await this.page.goto(url);
        console.log('Browser opened');
    }

    async waitForTimeout(timeout) {
        await this.page.waitForTimeout(timeout);
    }

    async close() {
        await this.browser.close();
    }

    async test() {
        await this.open('https://www.google.com');
        await this.waitForTimeout(5000);
        await this.close();
    }
}