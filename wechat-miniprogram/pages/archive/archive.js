const briefData = require("../../utils/issues");

Page({
  data: {
    archive: []
  },

  onLoad() {
    this.setData({
      archive: briefData.archive || []
    });
  },

  openIssue(event) {
    const { date } = event.currentTarget.dataset;
    const issue = briefData.issues[date];
    const firstSection = issue && issue.sections && issue.sections[0];

    if (!firstSection) {
      wx.showToast({ title: "暂无详情", icon: "none" });
      return;
    }

    wx.navigateTo({
      url: `/pages/detail/detail?date=${date}&id=${firstSection.id}`
    });
  }
});
