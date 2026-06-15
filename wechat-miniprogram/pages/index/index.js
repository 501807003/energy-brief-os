const briefStore = require("../../utils/brief-data");

function formatPrice(value) {
  return Number(value || 0).toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
}

function buildTariffWatch(items) {
  return (items || []).map((item) => ({
    ...item,
    shortLabel: String(item.label || "").replace("\u4eca\u65e5\u7535\u4ef7", ""),
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
    this.loadBriefData();
  },

  onShow() {
    this.loadBriefData();
  },

  loadBriefData() {
    briefStore.getBriefData().then((briefData) => {
      const issue = briefData.issues[briefData.latestDate];
      if (!issue) return;

      this.setData({
        issue,
        sections: issue.sections || [],
        priceWatch: issue.price_watch || [],
        tariffWatch: buildTariffWatch(issue.tariff_watch)
      });
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
