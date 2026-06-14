const briefData = require("../../utils/issues");

function formatPrice(value) {
  return Number(value || 0).toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
}

const CHART_WIDTH = 580;
const CHART_HEIGHT = 220;

function buildLineChart(points) {
  if (!points || points.length === 0) return { points: [], segments: [] };
  const values = points.map((point) => Number(point.value || 0));
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = Math.max(max - min, 0.012);
  const chartPoints = points.map((point, index) => {
    const value = Number(point.value || 0);
    const ratio = (value - min) / span;
    return {
      date: String(point.date || "").slice(5),
      valueText: formatPrice(value),
      level: point.level || "",
      left: points.length === 1 ? CHART_WIDTH / 2 : Math.round((index / (points.length - 1)) * CHART_WIDTH),
      bottom: Math.round(34 + ratio * (CHART_HEIGHT - 68))
    };
  });

  const segments = chartPoints.slice(0, -1).map((point, index) => {
    const next = chartPoints[index + 1];
    const dx = next.left - point.left;
    const dy = next.bottom - point.bottom;
    const width = Math.sqrt((dx * dx) + (dy * dy));
    const angle = -(Math.atan2(dy, dx) * 180 / Math.PI);
    return {
      left: point.left,
      bottom: point.bottom,
      width: Math.round(width),
      angle: angle.toFixed(2)
    };
  });

  return { points: chartPoints, segments };
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
      chart: buildLineChart(points)
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
