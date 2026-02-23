import requests
import xml.etree.ElementTree as ET
import datetime

# 配置信息
SITEMAP_URL = "https://www.juniutv.top/sitemap.xml"
DOMAIN = "juniutv.top"

def fetch_latest_links():
    try:
        res = requests.get(SITEMAP_URL, timeout=20)
        root = ET.fromstring(res.content)
        # 提取所有伪静态 .html 链接
        urls = [loc.text for loc in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc') if '.html' in loc.text]
        # 只取最新的 30 个，防止 README 过长被封
        return urls[:30]
    except:
        return []

def generate_readme(links):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    content = f"# 🚀 剧牛影视资源实时索引库\n\n"
    content += f"> 更新时间：{now} (自动同步)\n\n"
    content += f"## 🔗 官方入口\n* **[剧牛影视官网](https://{DOMAIN})**\n* **[站点地图索引](https://{DOMAIN}/sitemap.xml)**\n\n"
    content += "## 🎬 最新上线资源\n"
    
    for link in links:
        # 提取链接末尾作为简单描述，或者保持原样
        content += f"* [{link}]({link})\n"
    
    content += f"\n---\n**技术说明**：由 GitHub Actions 自动更新。主站部署于 {DOMAIN}。"
    return content

if __name__ == "__main__":
    links = fetch_latest_links()
    if links:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(generate_readme(links))
        print("README 已更新")
