const briefData = require("../../utils/issues");

Page({
  data: {
    archive: [],
    selectedDate: "",
    selectedIssue: null
  },

  onLoad() {
    const archive = (briefData.archive || []).map((item) => {
      const issue = briefData.issues[item.date] || {};
      const sections = issue.sections || [];

      return {
        ...item,
        summary: issue.daily_judgment || item.headline,
        sectionCount: sections.length,
        dayText: String(item.date || "").slice(8),
        monthText: String(item.date || "").slice(5, 7),
        sectionsPreview: sections.map((section, index) => ({
          id: section.id,
          label: section.label,
          indexText: index + 1 < 10 ? `0${index + 1}` : `${index + 1}`
        }))
      };
    });

    const selectedIssue = archive[0] || null;

    this.setData({
      archive,
      selectedDate: selectedIssue ? selectedIssue.date : "",
      selectedIssue
    });
  },

  selectIssue(event) {
    const { date } = event.currentTarget.dataset;
    const selectedIssue = this.data.archive.find((item) => item.date === date) || null;

    if (!selectedIssue) return;

    this.setData({
      selectedDate: date,
      selectedIssue
    });
  },

  openIssue(event) {
    const date = event.currentTarget.dataset.date || this.data.selectedDate;
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
