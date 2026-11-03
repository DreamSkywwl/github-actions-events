// #!/usr/bin/env node
/**
 * fuliba RSS 同步到 GitHub 仓库
 *
 * 功能：
 *   1. 依次尝试多个 fuliba feed 链接，获取到有效 XML 即停止，全部失败则 ShowDoc 微信推送告警；
 *   2. 解析 RSS XML，抽取出条目（title / link / pubDate / description）；
 *   3. 使用 Octokit 读取仓库中已有的 JSON 文件，对比链接去重；
 *   4. 新条目追加到最前面，写回 GitHub 仓库；
 *   5. 完成后通过 ShowDoc 推送执行结果（成功条数 / 失败告警）。
 *
 * 环境变量（GitHub Actions 中作为 secrets 注入）：
 *   GITHUB_TOKEN       GitHub Personal Access Token，需 repo 权限
 *   GITHUB_OWNER       仓库所有者（用户名或组织名）
 *   GITHUB_REPO        仓库名
 *   GITHUB_BRANCH      分支名，默认 main
 *   FILE_PATH          仓库内存储 RSS JSON 的路径，默认 data/fuliba.json
 */

const https = require('https');
const http = require('http');
const { Octokit } = require('@octokit/rest');

// ========== 配置 ==========
const FEED_URLS = [
    'https://fuliba2023.net/feed',
    'https://fuliba2025.net/feed',
    'https://fuliba.net/feed',
    'https://fuliba66.net/feed',
    'https://f.uliba.net/feed',
];

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const OWNER = process.env.GITHUB_OWNER;
const REPO = process.env.GITHUB_REPO;
const BRANCH = process.env.GITHUB_BRANCH || 'main';
const FILE_PATH = process.env.FILE_PATH || 'fuliba.json';
// const SHOWDOC_PUSH_URL = process.env.SHOWDOC_PUSH_URL;

const octokit = new Octokit({ auth: GITHUB_TOKEN });

// ========== 工具函数 ==========

/**
 * 简单封装 HTTP/HTTPS GET，返回字符串 body
 * 自动跟随 301/302 重定向
 */
function fetchText(url, redirectCount = 0) {
    return new Promise((resolve, reject) => {
        if (redirectCount > 5) {
            return reject(new Error(`重定向次数过多: ${url}`));
        }
        const lib = url.startsWith('https') ? https : http;
        const req = lib.get(
            url,
            {
                headers: {
                    'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                        '(KHTML, like Gecko) Chrome/124.0 Safari/537.36',
                    Accept: 'application/rss+xml, application/xml, text/xml, */*',
                },
                timeout: 15000,
            },
            (res) => {
                // 处理重定向
                if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
                    const nextUrl = new URL(res.headers.location, url).toString();
                    res.resume();
                    return fetchText(nextUrl, redirectCount + 1).then(resolve, reject);
                }
                if (res.statusCode < 200 || res.statusCode >= 300) {
                    res.resume();
                    return reject(new Error(`HTTP ${res.statusCode} for ${url}`));
                }
                const chunks = [];
                res.setEncoding('utf8');
                res.on('data', (c) => chunks.push(c));
                res.on('end', () => resolve(chunks.join('')));
            }
        );
        req.on('timeout', () => {
            req.destroy();
            reject(new Error(`请求超时: ${url}`));
        });
        req.on('error', reject);
    });
}

/**
 * ShowDoc 推送消息
 * 支持 GET 形式，title / content 作为 query 参数
 */
async function pushShowDoc(title, content) {
    showdocPin = process.env.SHOWDOC_PIN
    showdocToken = process.env.SHOWDOC_TOKEN
    // letserverToken = os.environ.get("LETSERVER_TOKEN")
    if (!showdocPin) {
        console.log('[ShowDoc] 未配置 showdocPin，跳过推送');
        return;
    }
    try {

        url = "https://push.showdoc.com.cn/server/api/push/" + showdocPin
        const u = new URL(url);
        u.searchParams.set('title', title);
        u.searchParams.set('content', content);
        u.searchParams.set('user_token', showdocToken);
        const text = await fetchText(u.toString());
        console.log('[ShowDoc] 推送结果:', text);
    } catch (err) {
        console.error('[ShowDoc] 推送失败:', err.message);
    }
}

/**
 * 从 RSS XML 中解析出 <item> 列表
 * 不依赖第三方库，用正则抽取字段，适配 fuliba feed 常见格式
 */
function parseRssItems(xml) {
    const items = [];
    // 匹配每个 <item>...</item>
    const itemRegex = /<item>([\s\S]*?)<\/item>/gi;
    let m;
    while ((m = itemRegex.exec(xml)) !== null) {
        const block = m[1];
        const getTag = (name) => {
            // 同时兼容 <![CDATA[...]]> 和直接文本
            const re = new RegExp(
                `<${name}[^>]*>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/${name}>`,
                'i'
            );
            const r = block.match(re);
            return r ? r[1].trim() : '';
        };
        const title = getTag('title');
        const link = getTag('link');
        const pubDate = getTag('pubDate');
        const description = getTag('description');
        if (title && link) {
            items.push({ title, link, pubDate, description });
        }
    }
    return items;
}

/**
 * 判断字符串是否像 XML（包含 <?xml 或 <rss 标签）
 */
function looksLikeXml(text) {
    if (!text) return false;
    const t = text.trim().toLowerCase();
    return t.startsWith('<?xml') || t.includes('<rss') || t.includes('<feed');
}

function formatToShanghaiTime(dateStr) {
    const date = new Date(dateStr);

    // 校验日期是否解析成功
    if (isNaN(date.getTime())) {
        throw new Error(`无效的日期格式: ${dateStr}`);
    }

    // 使用内置Intl API显式指定上海时区，24小时制
    const formatter = new Intl.DateTimeFormat('zh-CN', {
        timeZone: 'Asia/Shanghai',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false // 关闭12小时制
    });

    // 提取各时间字段，避免分隔符差异
    const timeParts = Object.fromEntries(
        formatter.formatToParts(date)
            .filter(part => part.type !== 'literal') // 过滤掉分隔符（/、:、空格等）
            .map(part => [part.type, part.value])
    );

    // 拼接为标准 年-月-日 时:分:秒 格式
    return `${timeParts.year}-${timeParts.month}-${timeParts.day} ${timeParts.hour}:${timeParts.minute}:${timeParts.second}`;
}

// ========== 主流程 ==========
async function main() {
    console.log('[Step1] 开始尝试获取 RSS feed ...');

    // ---- 功能2：按顺序尝试多个链接，取第一个有效 XML ----
    let xmlText = '';
    let usedUrl = '';
    const errors = [];

    for (const url of FEED_URLS) {
        try {
            console.log(`  尝试: ${url}`);
            const text = await fetchText(url);
            if (looksLikeXml(text)) {
                xmlText = text;
                usedUrl = url;
                console.log(`  ✓ 成功从 ${url} 获取到 XML`);
                break;
            } else {
                const msg = `${url} 返回内容不是 XML（长度=${text.length}，开头=${text.slice(0, 80).replace(/\n/g, '')}）`;
                console.warn(`  ✗ ${msg}`);
                errors.push(msg);
            }
        } catch (err) {
            console.warn(`  ✗ ${url} 请求失败: ${err.message}`);
            errors.push(`${url} → ${err.message}`);
        }
    }

    // 五个链接全部失败 → ShowDoc 推送告警
    if (!xmlText) {
        const errMsg =
            'fuliba RSS 抓取失败，以下 5 个链接均未获取到有效 XML：\n\n' +
            errors.map((e, i) => `${i + 1}. ${e}`).join('\n');
        console.error(errMsg);
        await pushShowDoc('fuliba RSS 抓取失败告警', errMsg);
        process.exitCode = 1;
        return;
    }

    // ---- 解析 XML ----
    const items = parseRssItems(xmlText);
    console.log(`[Step2] 从 ${usedUrl} 解析到 ${items.length} 条 item`);
    if (items.length === 0) {
        await pushShowDoc(
            'fuliba RSS 解析结果异常',
            `成功获取到 XML（来源 ${usedUrl}），但未解析出任何 <item>，请检查源站格式是否变化。`
        );
        return;
    }
    // console.log('items>-->:', JSON.stringify(items));
    // return
    // ---- 功能3：读取 GitHub 上已有 JSON，去重合并 ----
    console.log(`[Step3] 读取 GitHub 上已有文件 ${OWNER}/${REPO}/${FILE_PATH} ...`);
    let existing = [];
    let existingSha = null;

    try {
        const { data } = await octokit.rest.repos.getContent({
            owner: OWNER,
            repo: REPO,
            path: FILE_PATH,
            ref: BRANCH,
        });
        existingSha = data.sha;
        const decoded = Buffer.from(data.content, 'base64').toString('utf8');
        existing = JSON.parse(decoded);
        if (!Array.isArray(existing)) existing = [];
        console.log(`  已有 ${existing.length} 条记录`);
    } catch (err) {
        if (err.status === 404) {
            console.log('  文件不存在，将新建');
        } else {
            console.warn('  读取文件失败，将作为新文件创建：', err.message);
        }
    }

    const existingLinks = new Set(existing.map((i) => i.link));
    const newItems = items.filter((i) => !existingLinks.has(i.link));
    console.log(`  本次新增 ${newItems.length} 条`);

    // ---- 写回 GitHub ----
    const merged = [...newItems, ...existing];
    const contentStr = JSON.stringify(merged, null, 2);
    const commitMsg =
        newItems.length > 0
            ? `chore(data): 同步 fuliba RSS，新增 ${newItems.length} 条（${new Date().toISOString().slice(0, 10)}）`
            : `chore(data): fuliba RSS 检查，无新增（${new Date().toISOString().slice(0, 10)}）`;

    await octokit.rest.repos.createOrUpdateFileContents({
        owner: OWNER,
        repo: REPO,
        path: FILE_PATH,
        message: commitMsg,
        content: Buffer.from(contentStr).toString('base64'),
        sha: existingSha || undefined, // 新建时不传 sha
        branch: BRANCH,
    });
    console.log(`  ✓ 文件已写入 GitHub，commit: ${commitMsg}`);

    // ---- 功能4：ShowDoc 推送结果 ----
    if (newItems.length > 0) {
        const pushTitle = '您有一个新消息'

        let contentValue = ''
        for (var indez = 0; indez < newItems.length; indez++) {
            let forTmp = newItems[indez];
            contentValue += `${forTmp.title}(时间：${formatToShanghaiTime(forTmp.pubDate)})  地址：${forTmp.link}\n`
        }
        /* const pushContent =
            `数据来源：${usedUrl}\n` +
            `仓库文件：${OWNER}/${REPO}/${FILE_PATH}\n` +
            `分支：${BRANCH}\n` +
            `本次抓取：${items.length} 条\n` +
            `新增条目：${newItems.length} 条\n` +
            `库内总计：${merged.length} 条\n\n` +
            (newItems.length > 0
                ? '最新条目：\n' +
                newItems
                    .slice(0, 10)
                    .map((it, i) => `${i + 1}. ${it.title}\n   ${it.link}`)
                    .join('\n')
                : '没有发现新条目。'); */

        await pushShowDoc(pushTitle, contentValue);
    }
    /* const pushTitle =
        newItems.length > 0
            ? `fuliba RSS 同步成功，新增 ${newItems.length} 条`
            : 'fuliba RSS 同步完成，无新内容'; */

    console.log('[Done] 全部流程结束');
}

main().catch(async (err) => {
    console.error('[Fatal]', err);
    await pushShowDoc('fuliba RSS 同步脚本异常', `执行出错：${err.stack || err.message}`);
    process.exitCode = 1;
});
