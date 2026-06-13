const briefData = require("../../utils/issues");

function buildLine(points, width = 520, height = 150) {
  if (!points || points.length === 0) return "";
  if (points.length === 1) {
    const y = height - (points[0].value / 100) * height;
    return `${width},${y.toFixed(1)}`;
  }

  return points.map((point, index) => {
    const x = (index / (points.length - 1)) * width;
    const y = height - (point.value / 100) * height;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(" ");
}

Page({
  data: {
    trend: []
  },

  onLoad() {
    const trend = (briefData.priceTrend || []).map((item) => {
      const points = item.points || [];
      const first = points[0] ? points[0].value : item.latestValue;
      const delta = item.latestValue - first;
      return {
        ...item,
        line: buildLine(points),
        deltaText: delta > 0 ? `+${delta}` : `${delta}`,
        dates: points.map((point) => point.date.slice(5)).join(" / "),
        bars: points.map((point) => ({
          date: point.date.slice(5),
          value: point.value,
          height: Math.max(18, point.value * 1.35)
        }))
      };
    });

    this.setData({ trend });
  }
});
