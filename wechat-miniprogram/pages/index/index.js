const briefData = require("../../utils/issues");

function formatPrice(value) {
  return Number(value || 0).toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
}

function buildTariffWatch(items) {
  return (items || []).map((item) => ({
    ...item,
    shortLabel: String(item.label || "").replace("今日电价", ""),
    valueText: formatPrice(item.value)
  }));
}

Page({
  data: {
    issue: null,
    sections: [],
    priceWatch: [],
    tariffWatch: []
  },

  onLoad() {
    const issue = briefData.issues[briefData.latestDate];
    this.setData({
      issue,
      sections: issue.sections || [],
      priceWatch: issue.price_watch || [],
      tariffWatch: buildTariffWatch(issue.tariff_watch)
    });
  },

  openSection(event) {
    const { id, date } = event.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/detail/detail?date=${date}&id=${id}`
    });
  },

  openArchive() {
    wx.navigateTo({
      url: "/pages/archive/archive"
    });
  },

  openPriceTrend() {
    wx.navigateTo({
      url: "/pages/price/price"
    });
  }
});
