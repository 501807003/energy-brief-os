const briefData = require("../../utils/issues");

Page({
  data: {
    issue: null,
    section: null,
    rank: "01"
  },

  onLoad(options) {
    const date = options.date || briefData.latestDate;
    const issue = briefData.issues[date] || briefData.issues[briefData.latestDate];
    const sections = issue.sections || [];
    const sectionIndex = Math.max(0, sections.findIndex((item) => item.id === options.id));
    const section = sections[sectionIndex] || sections[0];

    this.setData({
      issue,
      section,
      rank: sectionIndex + 1 < 10 ? `0${sectionIndex + 1}` : `${sectionIndex + 1}`
    });
  },

  copySource() {
    const url = this.data.section && this.data.section.url;
    if (!url) {
      wx.showToast({ title: "暂无链接", icon: "none" });
      return;
    }

    wx.setClipboardData({
      data: url,
      success: () => {
        wx.showToast({ title: "原文链接已复制", icon: "success" });
      }
    });
  }
});
