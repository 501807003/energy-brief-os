const briefStore = require("../../utils/brief-data");

function ensureList(value, fallback) {
  if (Array.isArray(value) && value.length) return value;
  if (typeof value === "string" && value) return [value];
  return fallback || [];
}

function enrichSection(section) {
  if (!section) return null;

  return {
    ...section,
    what_happened: ensureList(section.what_happened, [section.summary].filter(Boolean)),
    industry_impact: ensureList(section.industry_impact, [section.why_it_matters].filter(Boolean)),
    watch_points: ensureList(section.watch_points, section.tags || []),
    term_explain: section.term_explain || {
      term: section.label || "\u5173\u952e\u8bcd",
      explain: section.why_it_matters || section.summary || "\u8fd9\u6761\u8d44\u8baf\u4e0e\u65b0\u80fd\u6e90\u9879\u76ee\u3001\u4ef7\u683c\u3001\u5e76\u7f51\u6216\u653f\u7b56\u5224\u65ad\u6709\u5173\u3002"
    }
  };
}

Page({
  data: {
    issue: null,
    section: null,
    sections: [],
    priceWatch: [],
    learningCard: null,
    isIssueMode: false,
    rank: "01"
  },

  onLoad(options) {
    this.options = options || {};
    this.loadBriefData();
  },

  loadBriefData() {
    briefStore.getBriefData().then((briefData) => {
      const options = this.options || {};
      const date = options.date || briefData.latestDate;
      const issue = briefData.issues[date] || briefData.issues[briefData.latestDate];
      if (!issue) return;

      const sections = (issue.sections || []).map(enrichSection);
      const isIssueMode = options.mode === "issue" || !options.id;
      const sectionIndex = Math.max(0, sections.findIndex((item) => item.id === options.id));
      const section = sections[sectionIndex] || sections[0];

      this.setData({
        issue,
        section,
        sections,
        priceWatch: issue.price_watch || [],
        learningCard: issue.learning_card || null,
        isIssueMode,
        rank: sectionIndex + 1 < 10 ? `0${sectionIndex + 1}` : `${sectionIndex + 1}`
      });
    });
  },

  openSection(event) {
    const { id } = event.currentTarget.dataset;
    const issue = this.data.issue;
    if (!issue || !id) return;

    wx.navigateTo({
      url: `/pages/detail/detail?date=${issue.date}&id=${id}`
    });
  },

  copyIssueSource(event) {
    const { url } = event.currentTarget.dataset;
    if (!url) {
      wx.showToast({ title: "\u6682\u65e0\u94fe\u63a5", icon: "none" });
      return;
    }

    wx.setClipboardData({
      data: url,
      success: () => {
        wx.showToast({ title: "\u539f\u6587\u94fe\u63a5\u5df2\u590d\u5236", icon: "success" });
      }
    });
  },

  copySource() {
    const url = this.data.section && this.data.section.url;
    if (!url) {
      wx.showToast({ title: "\u6682\u65e0\u94fe\u63a5", icon: "none" });
      return;
    }

    wx.setClipboardData({
      data: url,
      success: () => {
        wx.showToast({ title: "\u539f\u6587\u94fe\u63a5\u5df2\u590d\u5236", icon: "success" });
      }
    });
  }
});
