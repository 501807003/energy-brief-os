const briefData = require("../../utils/issues");

function formatPrice(value) {
  return Number(value || 0).toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
}

function buildBars(points) {
  if (!points || points.length === 0) return [];
  const values = points.map((point) => Number(point.value || 0));
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = Math.max(max - min, 0.012);
  return points.map((point) => {
    const value = Number(point.value || 0);
    const ratio = (value - min) / span;
    return {
      date: String(point.date || "").slice(5),
      valueText: formatPrice(value),
      level: point.level || "",
      height: Math.round(72 + ratio * 120),
      offset: Math.round((1 - ratio) * 120)
    };
  });
}

function buildTrend(rawTrend, rangeDays) {
  return (rawTrend || []).map((item) => {
    const allPoints = item.points || [];
    const points = allPoints.slice(-rangeDays);
    const first = points[0] ? Number(points[0].value || 0) : Number(item.latestValue || 0);
    const latest = points.length ? Number(points[points.length - 1].value || 0) : Number(item.latestValue || 0);
    const delta = latest - first;
    return {
      ...item,
      points,
      latestValue: latest,
      latestValueText: formatPrice(latest),
      deltaText: `${delta >= 0 ? "+" : ""}${delta.toFixed(3)}`,
      directionText: delta > 0 ? "上行" : (delta < 0 ? "下行" : "持平"),
      rangeText: `近 ${rangeDays} 日，已记录 ${points.length} 天`,
      dates: points.map((point) => String(point.date || "").slice(5)).join(" / "),
      bars: buildBars(points)
    };
  });
}

Page({
  data: {
    trend: [],
    rangeDays: 7,
    rangeOptions: [
      { label: "近 7 日", value: 7 },
      { label: "近 30 日", value: 30 }
    ]
  },

  onLoad() {
    this.refreshTrend(7);
  },

  setRange(event) {
    const rangeDays = Number(event.currentTarget.dataset.range || 7);
    this.refreshTrend(rangeDays);
  },

  refreshTrend(rangeDays) {
    const trend = buildTrend(briefData.priceTrend || [], rangeDays);
    this.setData({ trend, rangeDays });
  }
});
