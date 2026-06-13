const briefData = require("../../utils/issues");

Page({
  data: {
    issue: null,
    sections: [],
    priceWatch: []
  },

  onLoad() {
    const issue = briefData.issues[briefData.latestDate];
    this.setData({
      issue,
      sections: issue.sections || [],
      priceWatch: issue.price_watch || []
    });
  },

  openSection(event) {
    const { id, date } = event.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/detail/detail?date=${date}&id=${id}`
    });
  },

  openSource(event) {
    const { url, title } = event.currentTarget.dataset;
    if (!url) {
      wx.showToast({ title: "暂无原文链接", icon: "none" });
      return;
    }

    wx.navigateTo({
      url: `/pages/webview/webview?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title || "原文")}`
    });
  },

  openArchive() {
    wx.navigateTo({
      url: "/pages/archive/archive"
    });
  }
});
