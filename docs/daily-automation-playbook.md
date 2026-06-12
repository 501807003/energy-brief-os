# 新能源简报每日自动化更新规程

这个仓库用于生成公开网页日报：https://501807003.github.io/energy-brief-os/

## 每天早上更新目标

每天生成一份新的新能源日报，覆盖 6 个固定方向：

- 光伏价格与产业链：硅料、硅片、电池片、组件、分布式、集中式项目。
- 风电项目与招标：陆风、海风、整机招标、中标价、并网节点。
- 储能与调峰政策：独立储能、共享储能、容量补偿、调峰补偿、辅助服务。
- 变电站与并网消纳：接入系统、送出工程、升压站、主网消纳能力。
- 电力交易与电价：机制电价、绿电交易、绿证、现货价差、中长期交易。
- 国家与地方新能源政策：国家能源局、发改委、省级能源局、电力交易中心文件。

## 推荐信息源

优先使用官方、权威和可公开转发的来源：

- 国家能源局：https://www.nea.gov.cn/
- 国家发展改革委：https://www.ndrc.gov.cn/
- 各省能源局、发改委官网。
- 各省电力交易中心官网。
- 北极星太阳能光伏网、北极星风力发电网、北极星储能网。
- 索比光伏网、光伏们、风电头条等行业媒体。

使用 `news-extractor` 时，只对明确文章 URL 做内容提取；搜索和筛选可以先用公开网页搜索完成。

## 原文链接要求

每个 `sections[*].url` 必须指向具体新闻、政策、公告或文章详情页，不能只填官网首页、栏目首页或搜索结果页。例如不能使用 `https://www.nea.gov.cn/` 作为详情链接。若官方首页只有栏目入口，需要继续点进具体文章；如果找不到对应详情页，就换一个有具体 URL 的权威来源。

## 数据更新要求

每天新增一个文件：`data/YYYY-MM-DD.json`。

必须包含：

- `date`、`weekday`、`generated_at`
- `headline`
- `hero_line_zh`，保持为 `每天早上<br>读懂新能源`
- `daily_judgment`
- `sections`，必须包含 `solar`、`wind`、`storage`、`grid`、`market`、`policy`
- `sections[*].url` 必须是具体文章链接，不能是官网首页。
- `price_watch`，至少 4 条
- `learning_card`
- `source_links`

所有可见文字必须是中文。不要恢复旧英文句子。

## 生成与校验

更新 JSON 后运行：

```powershell
python scripts/generate_daily.py
python scripts/validate_site.py
```

校验通过后，必须确认：

- `index.html` 是最新日期。
- `daily/YYYY-MM-DD.html` 已生成。
- `archive.html` 有最新日期链接。
- 页面链接带 `styles.css?v=`，避免公网缓存旧样式。
- 首屏 6 个方向可点击跳转。
- “查看原文”是蓝色按钮，不是普通下划线链接。
- 没有乱码，例如 `鏂`、`姣`、`锛`、`�`。

## 样式保护

不要把页面改回普通表格、后台仪表盘或纯列表。当前视觉方向是：

- Apple 官网产品页风格。
- 大标题、足够留白、柔和卡片。
- 第二部分保持 3 列 × 2 行，移动端自动变 1 列。
- 详情区保持左侧正文、右侧价格观察和每日概念。

只有在明确要改版时才调整 `assets/styles.css`。

## 发布

校验通过后提交并推送：

```powershell
git add .
git commit -m "Publish daily energy brief YYYY-MM-DD"
$tmp = New-TemporaryFile; $env:GIT_CONFIG_GLOBAL = $tmp.FullName; git push
```

推送后 GitHub Pages 会自动部署。
