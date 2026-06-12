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

  openArchive() {
    wx.navigateTo({
      url: "/pages/archive/archive"
    });
  }
});
