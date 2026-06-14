const briefData = require("../../utils/issues");

Page({
  data: {
    archive: []
  },

  onLoad() {
    const archive = (briefData.archive || []).map((item) => {
      const issue = briefData.issues[item.date] || {};
      const sections = issue.sections || [];

      return {
        ...item,
        summary: issue.daily_judgment || item.headline,
        sectionCount: sections.length,
        sectionsPreview: sections.map((section, index) => ({
          id: section.id,
          label: section.label,
          indexText: index + 1 < 10 ? `0${index + 1}` : `${index + 1}`
        }))
      };
    });

    this.setData({
      archive
    });
  },

  openIssue(event) {
    const { date } = event.currentTarget.dataset;
    const issue = briefData.issues[date];

    if (!issue) {
      wx.showToast({ title: "暂无详情", icon: "none" });
      return;
    }

    wx.navigateTo({
      url: `/pages/detail/detail?date=${date}&mode=issue`
    });
  }
});
