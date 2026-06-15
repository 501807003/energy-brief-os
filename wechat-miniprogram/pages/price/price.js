const briefStore = require("../../utils/brief-data");

function formatPrice(value) {
  return Number(value || 0).toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
}

const CHART_WIDTH = 580;
const CHART_HEIGHT = 220;
const CHART_PADDING = 56;
const POINT_GAP = 92;

function buildLineChart(points) {
  if (!points || points.length === 0) return { width: CHART_WIDTH, scrollable: false, points: [], segments: [] };
  const chartWidth = Math.max(CHART_WIDTH, ((points.length - 1) * POINT_GAP) + (CHART_PADDING * 2));
  const plotWidth = chartWidth - (CHART_PADDING * 2);
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
      left: points.length === 1 ? Math.round(chartWidth / 2) : Math.round(CHART_PADDING + ((index / (points.length - 1)) * plotWidth)),
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

  return { width: chartWidth, scrollable: chartWidth > CHART_WIDTH, points: chartPoints, segments };
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
      directionText: delta > 0 ? "\u4e0a\u884c" : (delta < 0 ? "\u4e0b\u884c" : "\u6301\u5e73"),
      rangeText: `\u8fd1 ${rangeDays} \u65e5\uff0c\u5df2\u8bb0\u5f55 ${points.length} \u5929`,
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
      { label: "\u8fd1 7 \u65e5", value: 7 },
      { label: "\u8fd1 30 \u65e5", value: 30 }
    ]
  },

  onLoad() {
    this.loadBriefData(7);
  },

  loadBriefData(rangeDays) {
    briefStore.getBriefData().then((briefData) => {
      this.briefData = briefData;
      this.refreshTrend(rangeDays);
    });
  },

  setRange(event) {
    const rangeDays = Number(event.currentTarget.dataset.range || 7);
    this.refreshTrend(rangeDays);
  },

  refreshTrend(rangeDays) {
    const briefData = this.briefData || briefStore.getCachedBriefData();
    const trend = buildTrend(briefData.priceTrend || [], rangeDays);
    this.setData({ trend, rangeDays });
  }
});
